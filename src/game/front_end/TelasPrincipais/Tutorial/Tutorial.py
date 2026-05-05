import pygame

from game.front_end.Componentes.Background import Background
from game.front_end.TelasPrincipais.Tutorial.Tutorial_layout import TutorialLayout
from game.front_end.TelasPrincipais.Tutorial.Tutorial_controller import TutorialController
from game.front_end.Componentes.Text import draw_text_centered, draw_text_raster
from game.front_end.helper.Responsive import Responsive
from game.front_end.Componentes.TelaSuspensa import TelaSuspensa
from system.preenchimento_e_textura.utils import PixelArrayClone
from system.primitivas.Linha import line_bresenham


class Tutorial:

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

        self.layout = TutorialLayout(width, height)
        self.controller = TutorialController()

        self.font_title = pygame.font.Font("assets/fonts/ThaleahFat.ttf", 48)
        self.font_body = pygame.font.Font("assets/fonts/ThaleahFat.ttf", 38)

    def update(self, input_handler):
        return self.controller.update(input_handler)

    def draw(self, surface):

        self.background.draw(surface)

        pixel_array = PixelArrayClone(surface)

        cx, cy = self.layout.get_center()
        medidas_painel, instructions_pos = self.layout.get_panel()
        center_x, center_y, w, h = medidas_painel
        color_bg = (45, 50, 65)

        painel_tutorial = TelaSuspensa(surface, center_x, center_y, w, h)
        painel_tutorial.fill(color_bg)
        painel_tutorial.draw((0,0,0), 3)

        draw_text_centered(
            pixel_array,
            self.font_title,
            "TUTORIAL",
            painel_tutorial,
            (255, 255, 255),
            "top_center"
        )

        # Collect all wrapped lines with equal spacing
        all_lines = []
        max_width = int(w * 0.9)
        spacing = self.resp.hp(0.055)
        start_y = self.resp.hp(0.15)

        for item in instructions_pos:
            words = item["text"].split(' ')
            current = ''
            for word in words:
                if current == '':
                    new_line = word
                else:
                    new_line = f"{current} {word}"
                line_width, _ = self.font_body.size(new_line)
                if line_width <= max_width:
                    current = new_line
                else:
                    if current:
                        all_lines.append(current)
                    current = word
            if current:
                all_lines.append(current)

        for i, line in enumerate(all_lines):
            y = start_y + i * spacing
            draw_text_raster(
                pixel_array,
                self.font_body,
                line,
                cx,
                y,
                (255, 255, 255),
                "center"
            )
        

        del pixel_array