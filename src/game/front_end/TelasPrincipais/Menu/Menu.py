import pygame

from game.front_end.TelasPrincipais.Menu.Menu_layout import MenuLayout
from game.front_end.TelasPrincipais.Menu.Menu_controller import MenuController

from game.front_end.Componentes.Button import Button
from game.front_end.Componentes.Text import draw_text_centered
from game.front_end.Componentes.Background import Background


class Menu:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.options = [
            "JOGAR",
            "ESTATISTICA",
            "SAIR"
        ]

        # ==================================================
        # Background
        # ==================================================

        self.background = Background(
            width,
            height,
            "assets/images/MenuBackground.jpeg"
        )

        # ==================================================
        # Layout e controller
        # ==================================================

        self.layout = MenuLayout(width, height, self.options)
        self.controller = MenuController(self.options)

        # ==================================================
        # Botões
        # ==================================================

        self.buttons = []
        self._create_buttons()

        # Fonte
        self.font = pygame.font.Font("assets/fonts/ThaleahFat.ttf", 36)

    # ======================================================
    # Cria botões
    # ======================================================

    def _create_buttons(self):

        buttons_layout = self.layout.get_buttons()

        for btn in buttons_layout:

            x, y, w, h = btn["rect"]

            button = Button(
                None,
                x,
                y,
                w,
                h,
                btn["text"]
            )

            self.buttons.append(button)

    # ======================================================
    # Update
    # ======================================================

    def update(self, input_handler):

        return self.controller.update(input_handler)

    # ======================================================
    # Draw
    # ======================================================

    def draw(self, surface):

        # 1️⃣ desenha background
        self.background.draw(surface)

        # 2️⃣ desenha botões
        pixel_array = pygame.PixelArray(surface)

        selected_index = self.controller.get_selected_index()

        for i, button in enumerate(self.buttons):

            button.surface = surface

            if i == selected_index:
                fill_color = (60, 60, 60)
                border_color = (255, 255, 255)
            else:
                fill_color = (30, 30, 30)
                border_color = (180, 180, 180)

            button.fill(fill_color)
            button.draw(border_color, 2)

            draw_text_centered(
                pixel_array,
                self.font,
                button.text,
                button,
                (255, 255, 255)
            )

        del pixel_array

    # ======================================================
    # Botão selecionado
    # ======================================================

    def get_selected(self):

        return self.controller.get_selected_index()