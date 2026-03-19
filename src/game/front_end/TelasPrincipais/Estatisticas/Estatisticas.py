import pygame

from game.front_end.Componentes.Background import Background
from game.front_end.TelasPrincipais.Estatisticas.Estatisticas_layout import StatisticsLayout
from game.front_end.TelasPrincipais.Estatisticas.Estatisticas_controller import StatisticsController
from game.front_end.Componentes.Text import draw_text_raster
from game.front_end.helper.responsive import Responsive


class Estatisticas:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.resp = Responsive(width, height)

        self.background = Background(
            width,
            height,
            "assets/images/PlainBackground.jpeg"
        )
        self.background.render_once()

        self.layout = StatisticsLayout(width, height)
        self.controller = StatisticsController()

        self.font = pygame.font.Font("assets/fonts/ThaleahFat.ttf", 48)

    def update(self, input_handler):
        return self.controller.update(input_handler)

    def draw(self, surface):

        self.background.draw(surface)

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