import pygame
from .Objeto import Objeto
from system.primitivas.Circulo import draw_circle_bresenham
from system.primitivas.Linha import line_bresenham
from system.preenchimento_e_textura.Preenchimento import scanline_fill_polygon, flood_fill
import math


class Coracao(Objeto):

    def __init__(self, x, y, size=28.0, speed=3.0):
        super().__init__(x, y, (220, 20, 60), speed, radius=size // 2)
        self.size = size

    def draw(self, screen):
        self._draw_heart(screen, int(self.x), int(self.y), self.size, self.color)

    def _draw_heart(self, surface, cx, cy, size, color):
        """
        Reaproveita a mesma lógica do componente de UI
        """

        r = max(2, int(size * 0.28))

        left_cx = cx - r
        right_cx = cx + r
        top_cy = cy - int(r * 0.2)

        bottom_x = cx
        bottom_y = cy + int(size * 0.45)

        # contorno
        draw_circle_bresenham(surface, left_cx, top_cy, r, color)
        draw_circle_bresenham(surface, right_cx, top_cy, r, color)

        line_bresenham(surface, left_cx - r, cy, bottom_x, bottom_y, color)
        line_bresenham(surface, right_cx + r, cy, bottom_x, bottom_y, color)
        line_bresenham(surface, left_cx - r, cy, right_cx + r, cy, color)

        # preenchimento
        try:
            def circle_polygon(cx0, cy0, radius, steps=24):
                verts = []
                for i in range(steps):
                    theta = 2 * math.pi * i / steps
                    vx = cx0 + radius * math.cos(theta)
                    vy = cy0 + radius * math.sin(theta)
                    verts.append((int(round(vx)), int(round(vy))))
                return verts

            left_poly = circle_polygon(left_cx, top_cy, r)
            right_poly = circle_polygon(right_cx, top_cy, r)

            tri = [
                (left_cx - r, cy),
                (bottom_x, bottom_y),
                (right_cx + r, cy)
            ]

            scanline_fill_polygon(surface, left_poly, color)
            scanline_fill_polygon(surface, right_poly, color)
            scanline_fill_polygon(surface, tri, color)

        except Exception:
            try:
                flood_fill(surface, cx, cy, color)
            except Exception:
                pass

    def on_collect(self, game_state):
        """
        Lógica principal:
        - Se vida < 3 → recupera 1
        - Se vida == 3 → ganha 250 pontos
        """

        if game_state.vida.lives < game_state.vida.max_lives:
            game_state.vida.lives += 1

            # atualiza UI
            if game_state.vida.coracoes:
                game_state.vida.coracoes.lives = game_state.vida.lives
                game_state.vida.coracoes.draw()
        else:
            game_state.registrar_acerto(50)