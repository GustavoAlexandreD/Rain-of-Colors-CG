import pygame
from .Objeto import Objeto

class Estrela(Objeto):

    def __init__(self, x, y):
        super().__init__(x, y, (255, 215, 0), speed=1.5, radius=10)

    def draw(self, screen):

        points = [
            (self.x, self.y - 10),
            (self.x + 4, self.y - 3),
            (self.x + 10, self.y),
            (self.x + 4, self.y + 3),
            (self.x, self.y + 10),
            (self.x - 4, self.y + 3),
            (self.x - 10, self.y),
            (self.x - 4, self.y - 3)
        ]

        pygame.draw.polygon(screen, self.color, points)

    def on_collect(self, game_state):

        game_state.star_power = True
        game_state.star_timer = 300  # frames (~5s)