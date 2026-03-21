import pygame
import math
from .Objeto import Objeto
from system.preenchimento_e_textura.Preenchimento import scanline_fill_polygon
from system.transformacoes_geometricas.Transformacoes_Geometricas import rotacao


class Gelo(Objeto):

    def __init__(self, x, y):
        super().__init__(x, y, (180, 220, 255), speed=2, radius=20)
        self.rotation_angle = 0  # ângulo em graus

    def update(self):
        """
        Atualiza posição do objeto (movimento da chuva) e rotação
        """
        self.y += self.speed
        self.rotation_angle = (self.rotation_angle + 3) % 360

    def draw(self, screen):

        def snowflake_points(cx, cy, r):
            pts = []

            # floco com 6 pontas (hexagonal)
            for i in range(6):
                angle = math.radians(i * 60)

                # ponta externa
                x_outer = cx + r * math.cos(angle)
                y_outer = cy + r * math.sin(angle)
                pts.append((x_outer, y_outer))

                # ponto interno (para dar forma de estrela)
                inner_angle = math.radians(i * 60 + 30)
                x_inner = cx + (r * 0.4) * math.cos(inner_angle)
                y_inner = cy + (r * 0.4) * math.sin(inner_angle)
                pts.append((x_inner, y_inner))

            return [(int(x), int(y)) for x, y in pts]

        # Gera pontos base do floco
        poly = snowflake_points(self.x, self.y, self.radius)
        
        # Aplica rotação ao redor do centro
        poly = rotacao(poly, self.rotation_angle, pivot=(self.x, self.y))
        poly = [(int(x), int(y)) for x, y in poly]

        try:
            scanline_fill_polygon(screen, poly, self.color)
            from system.primitivas.Linha import line_bresenham
            for i in range(len(poly)):
                x0, y0 = poly[i]
                x1, y1 = poly[(i + 1) % len(poly)]
                line_bresenham(screen, x0, y0, x1, y1, (0,0,0))
        except Exception:
            from system.primitivas.Linha import line_bresenham
            for i in range(len(poly)):
                x0, y0 = poly[i]
                x1, y1 = poly[(i + 1) % len(poly)]
                line_bresenham(screen, x0, y0, x1, y1, self.color)

    def on_collect(self, game_state):
        game_state.activate_freeze(180)