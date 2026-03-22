import pygame
from src.game.front_end.Componentes.Button import Button
from src.game.front_end.TelasPrincipais.Pause.Pause_layout import PauseLayout
from src.game.front_end.TelasPrincipais.Pause.Pause_controller import PauseController
from src.game.front_end.Componentes.Text import draw_text_centered, draw_text_raster
from src.game.front_end.helper.Responsive import Responsive
from src.game.front_end.Componentes.TelaSuspensa import TelaSuspensa
from src.system.primitivas.Linha import line_bresenham

class Pause:

    def __init__(self, surface, width, height):

        self.width = width
        self.height = height
        self.resp = Responsive(width, height)
        self.surface = surface

        self.options = ["CONTINUAR", "RECOMECAR", "VOLTAR P/ MENU"]

        self.layout = PauseLayout(width, height, self.options)
        self.controller = PauseController(self.options)

        self.buttons = []
        self._create_buttons()

        # Fonte responsiva
        self.font_title = pygame.font.Font(
            "assets/fonts/ThaleahFat.ttf",
            self.resp.font(80)
        )

        self.font_buttons = pygame.font.Font(
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

    def draw(self):

        pixel_array = pygame.PixelArray(self.surface)

        cx, cy = self.layout.get_center()
        medidas_painel = self.layout.get_panel()
        center_x, center_y, w, h = medidas_painel
        color_bg = (45, 50, 65)

        painel_pause = TelaSuspensa(self.surface, center_x, center_y, w, h)
        painel_pause.fill(color_bg)
        painel_pause.draw((0,0,0), 3)

        draw_text_raster(
            pixel_array,
            self.font_title,
            "Pause",
            center_x,
            center_y - h // 3,
            (255, 255, 255),
            "center"
        )
        selected_index = self.controller.get_selected_index()

        for i, button in enumerate(self.buttons):

            button.surface = self.surface

            selected = (i == selected_index)

            self.draw_button(button, selected)

            draw_text_centered(
                pixel_array,
                self.font_buttons,
                button.text,
                button,
                (255, 255, 255)
            )

        del pixel_array