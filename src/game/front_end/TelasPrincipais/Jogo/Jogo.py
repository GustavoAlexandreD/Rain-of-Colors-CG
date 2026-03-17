import pygame

from game.front_end.Componentes.Background import Background
from game.front_end.TelasPrincipais.Jogo.Jogo_layout import JogoLayout
from game.front_end.TelasPrincipais.Jogo.Jogo_controller import JogoController
from game.front_end.Componentes.Text import draw_text_raster


class Jogo:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # ==================================================
        # Background
        # ==================================================

        self.background = Background(
            width,
            height,
            "assets/images/JogoBackground.jpeg"
        )

        self.background.render_once()



        self.layout = JogoLayout(width, height)
        self.controller = JogoController()

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
            "GAME RUNNING",
            cx - 200,
            cy,
            (255, 255, 255)
        )

        del pixel_array