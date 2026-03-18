import random
import math
import pygame
from .Objeto import Objeto
from system.primitivas.Circulo import draw_circle_bresenham
from system.preenchimento_e_textura.Preenchimento import scanline_fill_polygon


class Gota(Objeto):

    COLORS = [
        (255, 0, 0),
        (0, 0, 255),
        (0, 255, 0),
        (255, 255, 0),
        (255, 0, 255)
    ]

    def __init__(self, x, y, speed=2):
        color = random.choice(self.COLORS)
        super().__init__(x, y, color, speed, radius=18)

    def draw(self, screen):

        def gota_poly(cx, cy, r):
            pts = []

            # 🔵 Parte de baixo (semi-círculo)
            for i in range(16):
                theta = math.pi * (i / 15)  # 0 → π
                px = cx + r * math.cos(theta)
                py = cy + r * math.sin(theta)
                pts.append((px, py))

            # 🔺 ponta da gota (topo)
            pts.append((cx, cy - 1.8 * r))

            return [(int(x), int(y)) for x, y in pts]

        poly = gota_poly(self.x, self.y, self.radius)

        try:
            scanline_fill_polygon(screen, poly, self.color)
        except Exception:
            # fallback simples
            draw_circle_bresenham(screen, int(self.x), int(self.y), self.radius, self.color)

    def on_collect(self, game_state):

        if self.color == game_state.current_color or game_state.star_power:
            game_state.score += 10
        else:
            game_state.lives -= 1