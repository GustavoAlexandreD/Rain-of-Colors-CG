import pygame

from game.front_end.Componentes.Background import Background
from game.front_end.TelasPrincipais.Jogo.Jogo_layout import JogoLayout
from game.front_end.TelasPrincipais.Jogo.Jogo_controller import JogoController
from game.front_end.Componentes.Text import draw_text_raster
from game.front_end.Componentes.Coracoes import Coracoes
from game.scripts.Rain import Rain


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

        # ==================================================
        # Layout e Controller
        # ==================================================
        self.layout = JogoLayout(width, height)
        self.controller = JogoController()

        # ==================================================
        # CONFIGURAÇÃO DA CHUVA (IMPORTANTE)
        # pula 60px da esquerda e 600px da direita
        # ==================================================
        self.layout.set_rain_area_with_margins(
            left_margin=60,
            right_margin=660,
            spawn_above=160
        )

        # ==================================================
        # Rain
        # ==================================================
        self.rain = Rain(width, height)

        x_min, x_max, spawn_above = self.layout.get_rain_area()
        self.rain.set_area(x_min, x_max, spawn_above)

        # ==================================================
        # Fonte
        # ==================================================
        self.font = pygame.font.Font("assets/fonts/ThaleahFat.ttf", 48)

    # ==================================================
    # UPDATE
    # ==================================================
    def update(self, input_handler):
        self.rain.update()
        return self.controller.update(input_handler)

    # ==================================================
    # DRAW
    # ==================================================
    def draw(self, surface):

        # background
        self.background.draw(surface)

        # chuva (antes da UI)
        self.rain.draw(surface)

        # corações
        top_left = self.layout.get_top_left(70, 60)
        coracoes = Coracoes(surface, pos=top_left, spacing=40, size=32)
        coracoes.draw()

        # texto via rasterização
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