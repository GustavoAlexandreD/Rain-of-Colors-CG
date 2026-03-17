import pygame

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

        self.background.render_once()

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
    
    def draw_button(self, button, selected):

        x, y, w, h = button.x, button.y, button.width, button.height

        # Cores
        color_bg = (70, 70, 100) if selected else (45, 50, 65)
        color_border_outer = (0, 0, 0)
        color_border_inner = (150, 155, 170)
        color_shadow_inner = (30, 35, 45)

        button = Button(button.surface, x, y, w, h)
        button.fill(color_bg)
        button.draw(color_border_outer, 3)

        # Cantos chanfrados
        c = 4

        # Linha de luz (topo)
        line_bresenham(
            button.surface,
            x + c,
            y + 2,
            x + w - c,
            y + 2,
            color_border_inner
        )

        # Linha de sombra (base)
        line_bresenham(
            button.surface,
            x + c,
            y + h - 2,
            x + w - c,
            y + h - 2,
            color_shadow_inner
        )

    # ======================================================
    # Update
    # ======================================================

    def update(self, input_handler):

        return self.controller.update(input_handler)

    # ======================================================
    # Draw
    # ======================================================

    def draw(self, surface):

        # 1️⃣ background (rápido agora)
        self.background.draw(surface)

        selected_index = self.controller.get_selected_index()

        for i, button in enumerate(self.buttons):

            button.surface = surface

            selected = (i == selected_index)

            self.draw_button(button, selected)

            pixel_array = pygame.PixelArray(surface)

            draw_text_centered(
                pixel_array,
                self.font,
                button.text,
                button,
                (255, 255, 255)
            )

        del pixel_array