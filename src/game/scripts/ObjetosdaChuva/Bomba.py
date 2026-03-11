import pygame
from .Objeto import Objeto

class Bomba(Objeto):

    def __init__(self, x, y):
        super().__init__(x, y, (40, 40, 40), speed=3, radius=9)

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )

        # pavio
        pygame.draw.line(
            screen,
            (255, 0, 0),
            (int(self.x), int(self.y - self.radius)),
            (int(self.x + 3), int(self.y - self.radius - 5)),
            2
        )

    def on_collect(self, game_state):

        game_state.lives = 0