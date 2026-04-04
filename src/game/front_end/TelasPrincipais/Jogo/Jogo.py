import pygame
from game.front_end.TelasPrincipais.Pause.Pause import Pause
from game.front_end.TelasPrincipais.GameOver.GameOver import GameOver
from game.front_end.helper.Responsive import Responsive
from game.front_end.Componentes.Background import Background
from game.front_end.TelasPrincipais.Jogo.Jogo_layout import JogoLayout
from game.front_end.TelasPrincipais.Jogo.Jogo_controller import JogoController
from game.front_end.Componentes.Text import draw_text_raster
from game.scripts.Rain import Rain
from game.scripts.player.Balde import Balde
from game.front_end.Componentes.Coracoes import Coracoes
from game.scripts.Vida import Vida
from game.scripts.GameState import GameState
from game.scripts.Rain import Rain
from game.scripts.player.Balde import Balde
from system.primitivas.Circulo import draw_filled_circle_bresenham
from system.transformacoes_geometricas.Janela_Viewport import Window, Viewport, world_to_viewport
from system.primitivas.Linha import line_bresenham


class Jogo:

    def __init__(self, width, height, surface):

        #Inicialização base
        self.width = width
        self.height = height
        self.surface = surface

        #Ajustes para responsividade
        self.resp = Responsive(width, height)

        #Background
        self.background = Background(
            width,
            height,
            "assets/images/PlainBackground.jpeg"
        )
        self.background.render_once()

        #Modularização da tela
        self.layout = JogoLayout(width, height)
        self.controller = JogoController()

        #Configurações de pontuação e vida
        base_x, base_y = self.layout.get_top_left()

        offset_x = self.resp.s(10)
        offset_y = self.resp.s(10)

        top_left = (base_x + offset_x, base_y + offset_y)

        heart_size = self.resp.s(26)  # baseado na escala
        heart_spacing = self.resp.s(35)

        self.coracoes = Coracoes(surface, pos=top_left, spacing=heart_spacing, size=heart_size)
        self.sistema_vida = Vida(coracoes=self.coracoes)
        self.game_state = GameState(self.sistema_vida)

        #Inicialização e limitação de espaço do balde e da chuva
        self.layout.set_rain_area_with_margins()

        x_min, x_max, spawn_above = self.layout.get_rain_area()

        self.rain = Rain(width, height)

        x_central = (x_min + x_max) // 2
        self.balde = Balde(self.game_state, x_central - 35, self.height - self.height//6, x_min, x_max)

        self.rain.set_area(x_min, x_max, spawn_above)
        self.balde.set_area(x_min, x_max)

        # Fonte responsiva
        self.font = pygame.font.Font(
            "assets/fonts/ThaleahFat.ttf",
            self.resp.font(68)
        )

        #Inicialização da janela de pause e game_over        
        self.pause = Pause(surface, width, height)
        self.game_over = GameOver(surface, width, height)

        # Configuração Viewport
        self.mundo = Window(x_min, -spawn_above, x_max, self.height)

        vp_w = self.resp.wp(0.22)
        vp_h = self.resp.hp(0.50) 
        vp_x = self.resp.wp(0.71) 
        vp_y = self.resp.hp(0.28)
        
        self.caixa_viewport = Viewport(vp_x, vp_y, vp_x + vp_w, vp_y + vp_h)

    def update(self, input_handler):
        if not self.controller.pause and self.sistema_vida.lives>0:
            self.game_state.update()
            self.rain.update(self.balde, self.game_state)
            self.balde.update(input_handler)
        return self.controller.update(input_handler)

    def draw(self, surface):

        self.background.draw(surface)
        self.rain.draw(surface)
        self.coracoes.draw()
        self.balde.draw(surface, 3)

        # ==========================================
        # 1. FUNDO DO PAINEL LATERAL E DIVISÓRIA
        # ==========================================
        linha_divisao_x = self.resp.wp(0.65)
        
        cor_fundo_painel = (30, 35, 45) # Cor de fundo

        pygame.draw.rect(surface, cor_fundo_painel, (linha_divisao_x, 0, self.width - linha_divisao_x, self.height)) # Colisão com a linha divisória

        # Linha divisória
        line_bresenham(surface, linha_divisao_x, 0, linha_divisao_x, self.height, (0, 0, 0))

        # ==========================================
        # 2. CAIXA DO VIEWPORT (MINIMAPA)
        # ==========================================
        vx1, vy1 = self.caixa_viewport.xmin, self.caixa_viewport.ymin
        vx2, vy2 = self.caixa_viewport.xmax, self.caixa_viewport.ymax
        
        # Borda da caixa
        cor_borda = (0, 0, 0)
        line_bresenham(surface, vx1, vy1, vx2, vy1, cor_borda) # Topo
        line_bresenham(surface, vx1, vy2, vx2, vy2, cor_borda) # Fundo
        line_bresenham(surface, vx1, vy1, vx1, vy2, cor_borda) # Esq
        line_bresenham(surface, vx2, vy1, vx2, vy2, cor_borda) # Dir

        # Linha de Visão (Onde a tela do jogador começa, Y = 0)
        _, y_visao = world_to_viewport(0, 0, self.mundo, self.caixa_viewport)
        line_bresenham(surface, vx1, y_visao, vx2, y_visao, (255, 0, 0))

        # Desenhar as Gotas no minimapa
        for obj in self.rain.objects:
            obj_vx, obj_vy = world_to_viewport(obj.x, obj.y, self.mundo, self.caixa_viewport)

            if vx1 + 5 < obj_vx < vx2 - 5 and vy1 + 5 < obj_vy < vy2 - 5:
                tipo = type(obj).__name__
                    
                if tipo == "Gota":
                    # Gota: Círculo normal com borda
                    draw_filled_circle_bresenham(surface, obj_vx, obj_vy, 3, obj.color, (0,0,0), 1)
                    
                elif tipo == "Bomba":
                    # Bomba: Agora é PRETA para destacar do fundo, com um pavio vermelho
                    draw_filled_circle_bresenham(surface, obj_vx, obj_vy, 4, (0, 0, 0), (255, 0, 0), 1)
                    line_bresenham(surface, obj_vx, obj_vy - 4, obj_vx + 2, obj_vy - 7, (255, 0, 0))
                    
                elif tipo == "Estrela":
                    # Estrela: Bolinha amarela com uma cruz de brilho branca
                    draw_filled_circle_bresenham(surface, obj_vx, obj_vy, 4, (255, 215, 0), (255, 255, 255), 1)
                    line_bresenham(surface, obj_vx - 5, obj_vy, obj_vx + 5, obj_vy, (255, 255, 255))
                    line_bresenham(surface, obj_vx, obj_vy - 5, obj_vx, obj_vy + 5, (255, 255, 255))
                    
                elif tipo == "Gelo":
                    # Gelo: Bolinha azul clara com um 'X' branco no meio
                    draw_filled_circle_bresenham(surface, obj_vx, obj_vy, 4, (180, 220, 255), (255, 255, 255), 1)
                    line_bresenham(surface, obj_vx - 3, obj_vy - 3, obj_vx + 3, obj_vy + 3, (255, 255, 255))
                    line_bresenham(surface, obj_vx - 3, obj_vy + 3, obj_vx + 3, obj_vy - 3, (255, 255, 255))
                    
                elif tipo == "Coracao":
                    # Coração: Bolinha vermelha com um pequeno 'V' rosa desenhado em cima
                    draw_filled_circle_bresenham(surface, obj_vx, obj_vy, 4, (220, 20, 60), (255, 182, 193), 1)
                    line_bresenham(surface, obj_vx - 3, obj_vy, obj_vx, obj_vy + 4, (255, 182, 193))
                    line_bresenham(surface, obj_vx + 3, obj_vy, obj_vx, obj_vy + 4, (255, 182, 193))

        # Desenhar o Balde no minimapa
        balde_vx, balde_vy = world_to_viewport(self.balde.x + self.balde.top_width//2, self.balde.y, self.mundo, self.caixa_viewport)
        draw_filled_circle_bresenham(surface, balde_vx, balde_vy, 5, (139,69,19), (0,0,0), 0)

        # ==========================================
        # 3. TEXTOS, PODERES E CÍRCULO DA COR (ALINHADOS)
        # ==========================================
        # ATENÇÃO: O PixelArray deve ser aberto APÓS o pygame.draw.rect do fundo!
        pixel_array = pygame.PixelArray(surface)
        
        centro_painel_x = self.caixa_viewport.xmin + (self.caixa_viewport.width // 2)

        # Posição inicial do SCORE abaixada para dar respiro
        y_atual_texto = self.resp.hp(0.06)

        texto_score = f"SCORE: {self.game_state.score:06d}"
        draw_text_raster(pixel_array, self.font, texto_score, centro_painel_x, y_atual_texto, (255, 255, 255), "center")
        y_atual_texto += self.resp.hp(0.08)

        if self.game_state.multiplier > 1:
            texto_combo = f"COMBO {self.game_state.multiplier}X"
            draw_text_raster(pixel_array, self.font, texto_combo, centro_painel_x, y_atual_texto, (255, 40, 0), "center")
            y_atual_texto += self.resp.hp(0.08)

        if self.game_state.freeze:
            texto_freeze = "FROZEN STATE!"
            draw_text_raster(pixel_array, self.font, texto_freeze, centro_painel_x, y_atual_texto, (230, 234, 225), "center")
            y_atual_texto += self.resp.hp(0.08)

        if self.game_state.star_power:
            texto_star = "STAR POWER!"
            draw_text_raster(pixel_array, self.font, texto_star, centro_painel_x, y_atual_texto, (255, 223, 0), "center")

        # Círculo da Cor Atual e texto "COR" posicionados em relação ao fundo do minimapa
        raio_cor = self.resp.s(40)
        y_cor = vy2 + self.resp.hp(0.12)
        
        draw_filled_circle_bresenham(
            surface, centro_painel_x, y_cor, raio_cor,
            fill_color=self.game_state.current_color, boundary_color=(0, 0, 0), boundary_thickness=6
        )

        draw_text_raster(pixel_array, self.font, "COR", centro_painel_x, y_cor - self.resp.hp(0.09), (255, 255, 255), "center")
        
        del pixel_array

        if self.controller.pause:
            self.pause.draw()
        
        if self.sistema_vida.lives <= 0:
            self.game_over.draw()