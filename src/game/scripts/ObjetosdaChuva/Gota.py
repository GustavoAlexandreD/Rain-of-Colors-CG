import random
import math
import pygame
from .Objeto import Objeto
from system.primitivas.Circulo import draw_circle_bresenham
from system.preenchimento_e_textura.Preenchimento import scanline_fill_polygon

class Gota(Objeto):

    COLORS = [
        (255, 0, 0),    # vermelho
        (0, 0, 255),    # azul
        (0, 255, 0),    # verde
        (255, 255, 0),  # amarelo
        (255, 0, 255)   # roxo
    ]

    def __init__(self, x, y, speed=2):
        color = random.choice(self.COLORS)
        # aumentar consideravelmente o tamanho das gotas
        super().__init__(x, y, color, speed, radius=18)

    def draw(self, screen):

        # corpo da gota
        # approximar círculo por polígono e preencher
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
        except Exception:
            # fallback: desenhar contorno
            draw_circle_bresenham(screen, int(self.x), int(self.y), self.radius, self.color)

    def on_collect(self, game_state):

        # verifica se a cor bate
        if self.color == game_state.current_color or game_state.star_power:

            game_state.score += 10

        else:
            game_state.lives -= 1