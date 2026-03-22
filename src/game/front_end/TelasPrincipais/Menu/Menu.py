import pygame

from game.front_end.helper.Responsive import Responsive
from game.front_end.TelasPrincipais.Menu.Menu_layout import MenuLayout
from game.front_end.TelasPrincipais.Menu.Menu_controller import MenuController
from system.primitivas.Linha import line_bresenham
from game.front_end.Componentes.Button import Button
from game.front_end.Componentes.Text import draw_text_centered
from game.front_end.Componentes.Background import Background


class Menu:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.resp = Responsive(width, height)

        self.options = ["JOGAR", "TUTORIAL", "ESTATISTICA", "SAIR"]

        # Background
        self.background = Background(
            width,
            height,
            "assets/images/MenuBackground.jpeg"
        )
        self.background.render_once()

        self.layout = MenuLayout(width, height, self.options)
        self.controller = MenuController(self.options)

        self.buttons = []
        self._create_buttons()

        # Fonte responsiva
        self.font = pygame.font.Font(
            "assets/fonts/ThaleahFat.ttf",
            self.resp.font(48)
        )

    def _create_buttons(self):

        for btn in self.layout.get_buttons():

            x, y, w, h = btn["rect"]

            self.buttons.append(
                Button(None, x, y, w, h, btn["text"])
            )

    def draw_button(self, button, selected):

        x, y, w, h = button.x, button.y, button.width, button.height

        color_bg = (70, 70, 100) if selected else (45, 50, 65)

        button.fill(color_bg)
        button.draw((0, 0, 0), self.resp.s(3))

        c = self.resp.s(4)

        # Luz topo
        line_bresenham(
            button.surface,
            x + c,
            y + self.resp.s(2),
            x + w - c,
            y + self.resp.s(2),
            (150, 155, 170)
        )

        # Sombra base
        line_bresenham(
            button.surface,
            x + c,
            y + h - self.resp.s(2),
            x + w - c,
            y + h - self.resp.s(2),
            (30, 35, 45)
        )

    def update(self, input_handler):
        return self.controller.update(input_handler)

    def draw(self, surface):

        self.background.draw(surface)

        selected_index = self.controller.get_selected_index()

        pixel_array = pygame.PixelArray(surface)

        for i, button in enumerate(self.buttons):

            button.surface = surface

            selected = (i == selected_index)

            self.draw_button(button, selected)

            draw_text_centered(
                pixel_array,
                self.font,
                button.text,
                button,
                (255, 255, 255)
            )

        del pixel_array