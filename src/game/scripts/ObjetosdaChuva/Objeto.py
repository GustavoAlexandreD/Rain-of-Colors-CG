from abc import ABC, abstractmethod
import pygame

class Objeto(ABC):

    def __init__(self, x, y, color, speed=2, radius=8):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.radius = radius
        self.active = True

    def update(self):
        """
        Atualiza posição do objeto (movimento da chuva)
        """
        self.y += self.speed

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def on_collect(self, game_state):
        """
        Define o que acontece quando o jogador pega o objeto
        """
        pass

    def is_off_screen(self, screen_height):
        return self.y - self.radius > screen_height

    def get_rect(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )