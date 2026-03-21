import pygame

from game.front_end.Componentes.Background import Background
from game.front_end.TelasPrincipais.Estatisticas.Estatisticas_layout import StatisticsLayout
from game.front_end.TelasPrincipais.Estatisticas.Estatisticas_controller import StatisticsController
from game.front_end.Componentes.Text import draw_text_centered, draw_text_raster
from game.front_end.helper.Responsive import Responsive
from game.front_end.Componentes.TelaSuspensa import TelaSuspensa
from system.primitivas.Linha import line_bresenham


class Estatisticas:

    def __init__(self, width, height, pontuations):

        self.width = width
        self.height = height
        self.pontuations = pontuations

        self.resp = Responsive(width, height)

        self.background = Background(
            width,
            height,
            "assets/images/PlainBackground.jpeg"
        )
        self.background.render_once()

        self.layout = StatisticsLayout(width, height, pontuations)
        self.controller = StatisticsController()

        self.font = pygame.font.Font("assets/fonts/ThaleahFat.ttf", 48)

    def update(self, input_handler):
        return self.controller.update(input_handler)

    def draw(self, surface):

        self.background.draw(surface)

        pixel_array = pygame.PixelArray(surface)

        cx, cy = self.layout.get_center()
        medidas_painel, pontuations_pos = self.layout.get_panel()
        center_x, y, w, h = medidas_painel
        color_bg = (45, 50, 65)

        painel_estatisticas = TelaSuspensa(surface, center_x, y, w, h)
        painel_estatisticas.fill(color_bg)
        painel_estatisticas.draw((0,0,0), 3)

        draw_text_centered(
            pixel_array,
            self.font,
            "ESTATISTICAS",
            painel_estatisticas,
            (255, 255, 255),
            "top_center"
        )
        for dict in pontuations_pos:
            draw_text_raster(
                pixel_array,
                self.font,
                dict["text"],
                dict["x"],
                dict["y"],
                (255, 255, 255),
                "center"
            )
        

        del pixel_array