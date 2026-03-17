import pygame

from game.front_end.TelasPrincipais.Estatisticas.Estatisticas_layout import StatisticsLayout
from game.front_end.TelasPrincipais.Estatisticas.Estatisticas_controller import StatisticsController
from game.front_end.Componentes.Text import draw_text_raster


class Estatisticas:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.layout = StatisticsLayout(width, height)
        self.controller = StatisticsController()

        self.font = pygame.font.Font("assets/fonts/ThaleahFat.ttf", 48)

    def update(self, input_handler):
        return self.controller.update(input_handler)

    def draw(self, surface):

        pixel_array = pygame.PixelArray(surface)

        cx, cy = self.layout.get_center()

        draw_text_raster(
            pixel_array,
            self.font,
            "STATISTICS",
            cx - 200,
            cy,
            (255, 255, 255)
        )

        del pixel_array