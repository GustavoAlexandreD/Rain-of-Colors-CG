import pygame
import os

from system.preenchimento_e_textura.Texture_Mapping import scanline_texture_polygon


class Background:

    def __init__(self, width, height, image_path):

        self.width = width
        self.height = height

        # ==============================
        # Carrega textura
        # ==============================

        self.texture = pygame.image.load("assets\\images\\MenuBackground.jpeg").convert_alpha()

        self.tex_w = self.texture.get_width()
        self.tex_h = self.texture.get_height()

        # ==============================
        # Converte para matriz (otimiza acesso)
        # ==============================

        self.texture_matrix = [
            [self.texture.get_at((x, y)) for y in range(self.tex_h)]
            for x in range(self.tex_w)
        ]

    # ======================================================
    # Render do background
    # ======================================================

    def draw(self, surface):

        pixel_array = pygame.PixelArray(surface)

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

        del pixel_array