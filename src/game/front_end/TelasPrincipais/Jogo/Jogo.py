import pygame
from game.front_end.helper.Responsive import Responsive
from game.front_end.Componentes.Background import Background
from game.front_end.TelasPrincipais.Jogo.Jogo_layout import JogoLayout
from game.front_end.TelasPrincipais.Jogo.Jogo_controller import JogoController
from game.front_end.Componentes.Text import draw_text_raster
from system.primitivas.Circulo import draw_circle_bresenham, draw_filled_circle_bresenham
from system.preenchimento_e_textura.Preenchimento import boundary_fill, scanline_fill
from game.scripts.Rain import Rain
from game.scripts.player.Balde import Balde
from game.front_end.Componentes.Coracoes import Coracoes
from game.scripts.Vida import Vida
from game.scripts.GameState import GameState
from game.scripts.ObjetosdaChuva.Gota import Gota
from system.primitivas.Circulo import draw_filled_circle_bresenham
from game.scripts.Rain import Rain
from game.scripts.player.Balde import Balde


class Jogo:

    def __init__(self, width, height, surface):

        self.width = width
        self.height = height
        self.surface = surface

        self.resp = Responsive(width, height)

        self.background = Background(
            width,
            height,
            "assets/images/PlainBackground.jpeg"
        )
        self.background.render_once()

        self.layout = JogoLayout(width, height)
        self.controller = JogoController()

        # UI
        base_x, base_y = self.layout.get_top_left()

        # pequeno ajuste fino (responsivo)
        offset_x = self.resp.s(10)
        offset_y = self.resp.s(10)

        top_left = (base_x + offset_x, base_y + offset_y)

        heart_size = self.resp.s(26)  # baseado na escala
        heart_spacing = self.resp.s(35)

        self.coracoes = Coracoes(surface, pos=top_left, spacing=heart_spacing, size=heart_size)
        self.sistema_vida = Vida(coracoes=self.coracoes)
        self.game_state = GameState(self.sistema_vida)

        # Chuva responsiva
        self.layout.set_rain_area_with_margins()

        x_min, x_max, spawn_above = self.layout.get_rain_area()

        self.rain = Rain(width, height)
        self.balde = Balde(self.game_state, abs(x_max-x_min//2), self.height - self.height//6, x_min, x_max)

        self.rain.set_area(x_min, x_max, spawn_above)
        self.balde.set_area(x_min, x_max)
        # Fonte responsiva
        self.font = pygame.font.Font(
            "assets/fonts/ThaleahFat.ttf",
            self.resp.font(68)
        )

    def update(self, input_handler):
        self.game_state.update()
        self.rain.update(self.balde, self.game_state)
        self.balde.update(input_handler)
        if self.sistema_vida.lives <= 0:
            return True
        return self.controller.update(input_handler)

    def draw(self, surface):

        self.background.draw(surface)

        self.rain.draw(surface)

        self.coracoes.draw()

        self.balde.draw(surface, 3)

        minimo = min(int(self.width), int(self.height))
        radius = minimo // 12
        margin = minimo // 5

        draw_filled_circle_bresenham(
            surface,
            self.width - margin,
            self.height - margin,
            radius,
            fill_color=self.game_state.current_color,
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

        texto_score = f"SCORE: {self.game_state.score:06d}"
        draw_text_raster(
            pixel_array,
            self.font,
            texto_score,
            self.resp.wp(0.7),  # Posição X (lado direito da tela)
            self.resp.hp(0.05), # Posição Y (topo da tela)
            (255, 255, 255),    # Branco
            "center"
        )

        # 2. COMBO (Só mostra se for maior que 1)
        if self.game_state.multiplier > 1:
            texto_combo = f"COMBO {self.game_state.multiplier}X"
            draw_text_raster(
                pixel_array,
                self.font,
                texto_combo,
                self.resp.wp(0.7),  # Mesmo X do Score
                self.resp.hp(0.12), # Um pouco abaixo do Score
                (255, 40, 0),      
                "center"
            )

        if self.game_state.freeze:
            texto_freeze = "FROZEN STATE!"
            y_position = self.resp.hp(0.20) if self.game_state.multiplier > 1 else self.resp.hp(0.12)
            draw_text_raster(
                pixel_array,
                self.font,
                texto_freeze,
                self.resp.wp(0.7),  
                y_position, 
                (230, 234, 225),      
                "center"
            )

        if self.game_state.star_power:
            texto_star = "STAR POWER!"
            y_position = self.resp.hp(0.20) if self.game_state.multiplier > 1 else self.resp.hp(0.12)
            draw_text_raster(
                pixel_array,
                self.font,
                texto_star,
                self.resp.wp(0.7),  
                y_position, 
                (255, 223, 0),      
                "center"
            )

        del pixel_array