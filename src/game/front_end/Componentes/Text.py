from typing import Literal

from system.primitivas.GetPixel import get_pixel

def draw_text_raster(pixel_array, font, text, x, y, color, orientation: Literal["center"]| None = None):
        """
        Renderiza texto desenhando pixel por pixel.

        Args:
            pixel_array: O PixelArray da tela principal (bloqueado).
            font: A fonte pygame carregada.
            text: A string a ser escrita.
            x, y: Posição superior esquerda.
            color: A cor do texto.
            orientation: Se for dada por center, o valor de x representa o centro da tela, logo, é preciso ajustar o x para representar o canto superior esquerdo da palavra. Fazendo a palavra ficar centralizada. Por default é dado por None.
        """
        # Renderiza o texto numa superfície temporária (na memória, não na tela)
        text_surface = font.render(text, True, color)
        w, h = text_surface.get_width(), text_surface.get_height()

        # Obtém dimensões da tela para evitar erro de índice
        screen_w, screen_h = pixel_array.shape

        if orientation == "center":
            x = x - text_surface.get_width()//2

        # Itera sobre os pixels da superfície do texto
        for px in range(w):
            for py in range(h):
                # Pega a cor do pixel do texto
                curr_color = get_pixel(text_surface, px, py)

                # Só desenha se não for transparente
                if curr_color.a > 10:
                    draw_x = x + px
                    draw_y = y + py

                    # Verifica limites da tela (Clipping)
                    if 0 <= draw_x < screen_w and 0 <= draw_y < screen_h:
                        pixel_array[draw_x, draw_y] = curr_color


def draw_text_raster_wrapped(pixel_array, font, text, x, y, color, max_width, orientation: Literal["center"] | None = None, line_spacing: int = 2):
    """Renderiza texto com quebra de linha quando excede max_width."""

    if max_width <= 0:
        draw_text_raster(pixel_array, font, text, x, y, color, orientation)
        return

    words = text.split(' ')
    lines = []
    current = ''

    for word in words:
        if current == '':
            new_line = word
        else:
            new_line = f"{current} {word}"

        line_width, _ = font.size(new_line)
        if line_width <= max_width:
            current = new_line
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    line_height = font.get_linesize() + line_spacing

    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        line_width = line_surface.get_width()
        line_x = x

        if orientation == 'center':
            line_x = x - line_width // 2

        draw_text_raster(pixel_array, font, line, line_x, y + i * line_height, color)

# ------------------------------------------------------
# Texto centralizado dentro de um objeto
# ------------------------------------------------------

def draw_text_centered(pixel_array, font, text, object, color, orientation: Literal["middle_center","top_center"] | None = "middle_center"):

    text_surface = font.render(text, True, color)

    text_w = text_surface.get_width()
    text_h = text_surface.get_height()

    center_x, center_y = object.get_center()

    if orientation == "middle_center":
        x = center_x - text_w // 2
        y = center_y - text_h // 2

        draw_text_raster(pixel_array, font, text, x, y, color)
    elif orientation == "top_center":
        x = center_x - text_w // 2
        y = text_h + text_h // 4

        draw_text_raster(pixel_array, font, text, x, y, color)
         