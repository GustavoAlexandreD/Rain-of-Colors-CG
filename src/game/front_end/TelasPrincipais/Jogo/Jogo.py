import pygame

from game.front_end.helper.responsive import Responsive
from game.front_end.Componentes.Background import Background
from game.front_end.TelasPrincipais.Jogo.Jogo_layout import JogoLayout
from game.front_end.TelasPrincipais.Jogo.Jogo_controller import JogoController
from game.front_end.Componentes.Text import draw_text_raster
from game.front_end.Componentes.Coracoes import Coracoes
from system.primitivas.Circulo import draw_circle_bresenham, draw_filled_circle_bresenham
from system.preenchimento_e_textura.Preenchimento import boundary_fill, scanline_fill
from game.scripts.Rain import Rain
from src.game.scripts.player.Balde import Balde


class Jogo:

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

        self.layout = JogoLayout(width, height)
        self.controller = JogoController()

        # Chuva responsiva
        self.layout.set_rain_area_with_margins()

        self.rain = Rain(width, height)

        x_min, x_max, spawn_above = self.layout.get_rain_area()
        self.rain.set_area(x_min, x_max, spawn_above)

        # Fonte responsiva
        self.font = pygame.font.Font(
            "assets/fonts/ThaleahFat.ttf",
            self.resp.font(68)
        )

    def update(self, input_handler):
        self.rain.update()
        return self.controller.update(input_handler)

    def draw(self, surface):

        self.background.draw(surface)

        self.rain.draw(surface)

        # UI
        base_x, base_y = self.layout.get_top_left()

        # pequeno ajuste fino (responsivo)
        offset_x = self.resp.s(10)
        offset_y = self.resp.s(10)

        top_left = (base_x + offset_x, base_y + offset_y)

        heart_size = self.resp.s(26)  # baseado na escala
        heart_spacing = self.resp.s(35)

        Coracoes(
            surface,
            pos=top_left,
            spacing=heart_spacing,
            size=heart_size
        ).draw()

        balde = Balde(100, self.height - self.height//8)
        balde.draw(surface,(0,0,0),3)

        minimo = min(int(self.width), int(self.height))
        radius = minimo // 12
        margin = minimo // 5

        draw_filled_circle_bresenham(
            surface,
            self.width - margin,
            self.height - margin,
            radius,
            fill_color=(255, 255, 255),
            boundary_color=(0, 0, 0),
            boundary_thickness=6,
        )

        pixel_array = pygame.PixelArray(surface)

        draw_text_raster(
            pixel_array,
            self.font,
            "COR",
            self.width - margin,
            self.height - margin - 2*radius,
            (255, 255, 255),
            "center"
        )

        cx, cy = self.layout.get_center()

        draw_text_raster(
            pixel_array,
            self.font,
            "GAME RUNNING",
            cx - self.resp.wp(0.1),
            cy,
            (255, 255, 255)
        )

        del pixel_array