import pygame
from .Objeto import Objeto
from system.primitivas.Circulo import draw_circle_bresenham
from system.primitivas.Linha import line_bresenham
from system.preenchimento_e_textura.Preenchimento import scanline_fill_polygon
import math


class Bomba(Objeto):

    def __init__(self, x, y):
        # aumentar consideravelmente o tamanho da bomba
        super().__init__(x, y, (40, 40, 40), speed=6.0, radius=27.0)

    def draw(self, screen):

        # preencher o corpo circular da bomba aproximando por polígono
        def circle_poly(cx, cy, r, steps=24):
            pts = []
            for i in range(steps):
                theta = 2 * math.pi * i / steps
                px = int(round(cx + r * math.cos(theta)))
                py = int(round(cy + r * math.sin(theta)))
                pts.append((px, py))
            return pts

        poly = circle_poly(self.x, self.y, self.radius, steps=24)
        try:
            scanline_fill_polygon(screen, poly, self.color)
            draw_circle_bresenham(screen, int(self.x), int(self.y), self.radius, (0,0,0))
        except Exception:
            draw_circle_bresenham(screen, int(self.x), int(self.y), self.radius, self.color)

        # pavio: desenhar linha com primitives
        try:
            x0, y0 = int(self.x), int(self.y - self.radius)
            x1, y1 = int(self.x + 3), int(self.y - self.radius - 5)
            line_bresenham(screen, x0, y0, x1, y1, (255, 0, 0))
        except Exception:
            pass

    def on_collect(self, game_state):
        # mata direto
        while game_state.perder_vida():
            pass