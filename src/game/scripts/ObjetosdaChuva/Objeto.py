from abc import ABC, abstractmethod
import pygame

class Objeto(ABC):

    def __init__(self, x, y, color, speed=2.0, radius=8.0):
        self.x = x
        self.y = y
        self.color = color
        self.base_speed = speed
        self.speed = speed
        self.radius = radius
        self.active = True

    def update(self):
        """
        Atualiza posição do objeto (movimento da chuva)
        """
        self.y += self.speed

    def get_position(self):
        """
        Retorna a posição do objeto para verificar se entrou no balde
        """
        return self.x, self.y

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
        return self.y > screen_height - (screen_height * 0.04)

    def get_rect(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )