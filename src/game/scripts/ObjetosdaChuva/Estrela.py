import pygame
from .Objeto import Objeto
from system.preenchimento_e_textura.Preenchimento import scanline_fill_polygon


class Estrela(Objeto):

    def __init__(self, x, y):
        # aumentar consideravelmente o tamanho da estrela
        super().__init__(x, y, (255, 215, 0), speed=1.5, radius=48)

    def draw(self, screen):

        points = [
            (int(self.x), int(self.y - 10)),
            (int(self.x + 4), int(self.y - 3)),
            (int(self.x + 10), int(self.y)),
            (int(self.x + 4), int(self.y + 3)),
            (int(self.x), int(self.y + 10)),
            (int(self.x - 4), int(self.y + 3)),
            (int(self.x - 10), int(self.y)),
            (int(self.x - 4), int(self.y - 3))
        ]

        try:
            scanline_fill_polygon(screen, points, self.color)
        except Exception:
            # fallback: draw polygon outline using lines
            from system.primitivas.Linha import line_bresenham
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                line_bresenham(screen, x0, y0, x1, y1, self.color)

    def on_collect(self, game_state):

        game_state.star_power = True
        game_state.star_timer = 300  # frames (~5s)