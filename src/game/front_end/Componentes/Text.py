def draw_text_raster(pixel_array, font, text, x, y, color):
        """
        Renderiza texto desenhando pixel por pixel.

        Args:
            pixel_array: O PixelArray da tela principal (bloqueado).
            font: A fonte pygame carregada.
            text: A string a ser escrita.
            x, y: Posição superior esquerda.
            color: A cor do texto.
        """
        # Renderiza o texto numa superfície temporária (na memória, não na tela)
        text_surface = font.render(text, True, color)
        w, h = text_surface.get_width(), text_surface.get_height()

        # Obtém dimensões da tela para evitar erro de índice
        screen_w, screen_h = pixel_array.shape

        # Itera sobre os pixels da superfície do texto
        for px in range(w):
            for py in range(h):
                # Pega a cor do pixel do texto
                curr_color = text_surface.get_at((px, py))

                # Só desenha se não for transparente
                if curr_color.a > 10:
                    draw_x = x + px
                    draw_y = y + py

                    # Verifica limites da tela (Clipping)
                    if 0 <= draw_x < screen_w and 0 <= draw_y < screen_h:
                        pixel_array[draw_x, draw_y] = curr_color