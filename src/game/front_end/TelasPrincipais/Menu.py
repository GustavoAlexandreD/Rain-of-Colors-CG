import pygame
import os

from system.primitivas.Linha import line_bresenham
from system.primitivas.Circulo import draw_circle_bresenham
from system.primitivas.Elipse import ellipse_bresenham
from system.preenchimento_e_textura.Preenchimento import scanline_fill_polygon
from system.preenchimento_e_textura.Texture_Mapping import scanline_texture_polygon


class Menu:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.options = ["JOGAR", "ESTATISTICA", "SAIR"]
        self.selected = 0

        self.buttons = []

        # ==============================
        # Carrega textura do background
        # ==============================

        BASE_DIR = os.path.dirname(__file__)

        path = os.path.join(
            BASE_DIR,
            "..",
            "..",
            "..",
            "assets",
            "images",
            "MenuBackground.jpeg",
        )

        self.background_texture = pygame.image.load(path).convert_alpha()

        # Dimensões da textura
        self.tex_w = self.background_texture.get_width()
        self.tex_h = self.background_texture.get_height()

        # Converte textura para matriz de cores (acesso rápido)
        self.texture_matrix = [
            [self.background_texture.get_at((x, y)) for y in range(self.tex_h)]
            for x in range(self.tex_w)
        ]

        self._build_layout()

    # ======================================================
    # Layout
    # ======================================================

    def _build_layout(self):

        center_x = self.width // 2
        start_y = 350
        spacing = 80

        self.buttons = []

        for i in range(len(self.options)):

            w = 260
            h = 50

            x = center_x - w // 2
            y = start_y + i * spacing

            self.buttons.append((x, y, w, h))

    # ======================================================
    # Update
    # ======================================================

    def update(self, input_handler):

        if input_handler.menu_up:
            self.selected = (self.selected - 1) % len(self.options)

        if input_handler.menu_down:
            self.selected = (self.selected + 1) % len(self.options)

        if input_handler.mouse_click:

            mx, my = input_handler.mouse_pos

            for i, (x, y, w, h) in enumerate(self.buttons):

                if x <= mx <= x + w and y <= my <= y + h:
                    self.selected = i
                    return self.options[i]

        if input_handler.menu_select:
            return self.options[self.selected]

        return None

    # ======================================================
    # Desenha BACKGROUND com textura
    # ======================================================

    def draw_background(self, surface):

        # Cria acesso direto à memória da surface
        pixel_array = pygame.PixelArray(surface)

        # Polígono que cobre a tela inteira
        vertices_uv = [
            (0, 0, 0, 0),
            (self.width, 0, self.tex_w, 0),
            (self.width, self.height, self.tex_w, self.tex_h),
            (0, self.height, 0, self.tex_h),
        ]

        scanline_texture_polygon(
            pixel_array,
            self.width,
            self.height,
            vertices_uv,
            self.texture_matrix,
            self.tex_w,
            self.tex_h,
            method="standard",
        )

        # Libera o lock da surface
        del pixel_array

    # ======================================================
    # Desenha botão
    # ======================================================

    def draw_button(self, surface, rect, selected):

        x, y, w, h = rect

        # Cores
        color_bg = (100, 110, 130) if selected else (45, 50, 65)
        color_border_outer = (0, 0, 0)
        color_border_inner = (150, 155, 170)
        color_shadow_inner = (30, 35, 45)

        # Cantos chanfrados
        c = 4

        vertices = [
            (x + c, y),
            (x + w - c, y),
            (x + w, y + c),
            (x + w, y + h - c),
            (x + w - c, y + h),
            (x + c, y + h),
            (x, y + h - c),
            (x, y + c)
        ]

        # Preenchimento
        scanline_fill_polygon(surface, vertices, color_bg)

        # Contorno
        for i in range(len(vertices)):

            p1 = vertices[i]
            p2 = vertices[(i + 1) % len(vertices)]

            line_bresenham(
                surface,
                p1[0],
                p1[1],
                p2[0],
                p2[1],
                color_border_outer
            )

        # Linha de luz (topo)
        line_bresenham(
            surface,
            x + c,
            y + 2,
            x + w - c,
            y + 2,
            color_border_inner
        )

        # Linha de sombra (base)
        line_bresenham(
            surface,
            x + c,
            y + h - 2,
            x + w - c,
            y + h - 2,
            color_shadow_inner
        )

    # ======================================================
    # Render final
    # ======================================================

    def draw(self, surface):

        self.draw_background(surface)

        for i, rect in enumerate(self.buttons):

            self.draw_button(
                surface,
                rect,
                i == self.selected
            )