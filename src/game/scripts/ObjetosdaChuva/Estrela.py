import pygame
from .Objeto import Objeto
from system.preenchimento_e_textura.Preenchimento import scanline_fill_polygon
from system.transformacoes_geometricas.Transformacoes_Geometricas import escala
from system.clipping.Cohen_Sutherland import draw_clipped_line

class Estrela(Objeto):

    def __init__(self, x, y):
        super().__init__(x, y, (255, 215, 0), speed=1.5, radius=30.0)
        self.twinkle_phase = True

    def draw(self, surface):

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

        if self.twinkle_phase:
            points = escala(points, 1.1, 1.1, (self.x, self.y))
            self.twinkle_phase = False
        else:
            points = escala(points, 0.9, 0.9, (self.x,self.y))
            self.twinkle_phase = True

        # converter para int só no final (melhor prática)
        points = [(int(px), int(py)) for px, py in points]
        
        xmin, ymin = 0, 0
        xmax = int(surface.get_width() * 0.66)
        ymax = surface.get_height()

        try:
            scanline_fill_polygon(surface, points, self.color)
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                draw_clipped_line(surface, x0, y0, x1, y1, xmin, ymin, xmax, ymax, (0, 0, 0))
        except Exception:
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                draw_clipped_line(surface, x0, y0, x1, y1, xmin, ymin, xmax, ymax, self.color)

    def on_collect(self, game_state):
        game_state.activate_star(300)