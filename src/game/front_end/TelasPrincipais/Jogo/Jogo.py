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
from game.scripts.CheckCollisions import checar_colisao
from game.front_end.Componentes.Coracoes import Coracoes
from game.scripts.VIda import Vida
from game.scripts.GameState import GameState
from game.scripts.ObjetosdaChuva.Gota import Gota

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

        # Chuva responsiva
        self.layout.set_rain_area_with_margins()

        x_min, x_max, spawn_above = self.layout.get_rain_area()

        self.rain = Rain(width, height)
        self.balde = Balde(abs(x_max-x_min//2), self.height - self.height//6, x_min, x_max)

        self.rain.set_area(x_min, x_max, spawn_above)
        self.balde.set_area(x_min, x_max)
        # Fonte responsiva
        self.font = pygame.font.Font(
            "assets/fonts/ThaleahFat.ttf",
            self.resp.font(68)
        )
        self.coracoes = Coracoes(surface=self.surface, pos=(20, 20))
        self.sistema_vida = Vida(coracoes=self.coracoes)
        self.game_state = GameState(self.sistema_vida)

    def update(self, input_handler):
        self.game_state.update()
        self.rain.update(self.game_state)
        self.balde.update(input_handler)

        balde_x = self.balde.x
        balde_y = self.balde.y
        balde_largura = self.balde.top_width
        balde_altura = self.balde.height

        for obj in list(self.rain.objects):
            if isinstance(obj, Gota):
                obj_x = obj.x - obj.largura
                obj_y = obj.y - (obj.altura // 2)
                obj_largura = obj.largura * 2
                obj_altura = obj.altura
            else:
                obj_x = obj.x - obj.radius
                obj_y = obj.y - obj.radius
                obj_largura = obj.radius * 2
                obj_altura = obj.radius * 2

            bateu = checar_colisao(balde_x, balde_y, balde_largura, balde_altura, obj_x, obj_y, obj_largura, obj_altura)

            if bateu:
                obj.on_collect(self.game_state)

                if obj in self.rain.objects:
                    self.rain.objects.remove(obj)
                
                print(f"Placar: {self.game_state.score} | Combo: {self.game_state.multiplier}x | Vidas: {self.sistema_vida.lives}")
        if self.sistema_vida.lives <= 0:
            print("GAMER OVER!")
            return True
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

        self.coracoes.draw()

        self.balde.draw(surface,(0,0,0),3)

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
                (255, 215, 0),      # Dourado para destacar
                "center"
            )

        del pixel_array