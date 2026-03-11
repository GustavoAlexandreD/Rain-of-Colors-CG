import random
import pygame
from .Objeto import Objeto

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
        super().__init__(x, y, color, speed, radius=6)

    def draw(self, screen):

        # corpo da gota
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )

    def on_collect(self, game_state):

        # verifica se a cor bate
        if self.color == game_state.current_color or game_state.star_power:

            game_state.score += 10

        else:
            game_state.lives -= 1