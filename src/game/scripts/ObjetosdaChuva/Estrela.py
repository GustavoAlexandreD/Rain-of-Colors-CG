import pygame
from .Objeto import Objeto
from system.preenchimento_e_textura.Preenchimento import scanline_fill_polygon


class Estrela(Objeto):

    def __init__(self, x, y):
        super().__init__(x, y, (255, 215, 0), speed=1.5, radius=38)

    def draw(self, screen):

        # fator base (define o "formato original")
        base = 10  

        scale = self.radius / base  # escala proporcional

        points = [
            (self.x, self.y - 10 * scale),
            (self.x + 4 * scale, self.y - 3 * scale),
            (self.x + 10 * scale, self.y),
            (self.x + 4 * scale, self.y + 3 * scale),
            (self.x, self.y + 10 * scale),
            (self.x - 4 * scale, self.y + 3 * scale),
            (self.x - 10 * scale, self.y),
            (self.x - 4 * scale, self.y - 3 * scale)
        ]

        # converter para int só no final (melhor prática)
        points = [(int(px), int(py)) for px, py in points]

        try:
            scanline_fill_polygon(screen, points, self.color)
        except Exception:
            from system.primitivas.Linha import line_bresenham
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                line_bresenham(screen, x0, y0, x1, y1, self.color)

    def on_collect(self, game_state):
        game_state.star_power = True
        game_state.star_timer = 300