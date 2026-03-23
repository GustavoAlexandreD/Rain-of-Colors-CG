import random
import math
import pygame
from .Objeto import Objeto
from system.primitivas.Circulo import draw_circle_bresenham
from system.primitivas.Linha import line_bresenham
from system.preenchimento_e_textura.Preenchimento import scanline_fill_polygon


class Gota(Objeto):

    COLORS = [
        (255, 0, 0),
        (0, 0, 255),
        (0, 255, 0),
        (255, 255, 0),
        (255, 0, 255)
    ]

    def __init__(self, x, y, altura, largura, speed=3.5):
        color = random.choice(self.COLORS)
        super().__init__(x, y, color, speed, radius=18)
        self.altura = altura
        self.largura = largura

    def gota_poly_points(self):
        # 1. Ponto do Topo e da Base
        topo_x = self.x
        topo_y = int(self.y - self.altura / 2)

        base_x = self.x
        base_y = int(self.y + self.altura / 2)

        # 2. Pontos de controle (Os "ímãs" que puxam a barriga para os lados)
        ctrl_esq_x = int(self.x - self.largura)
        ctrl_esq_y = int(self.y + self.altura / 2)

        ctrl_dir_x = int(self.x + self.largura)
        ctrl_dir_y = int(self.y + self.altura / 2)

        pontos_gota = []
        resolucao = 20

        # 3. Metade Esquerda da Gota (Calcula do Topo descendo até à Base)
        for i in range(resolucao + 1):  # Vai de 0 até à resolução
            t = i / resolucao
            t_inv = 1.0 - t

            x_atual = (t_inv**2 * topo_x) + (2 * t_inv * t * ctrl_esq_x) + (t**2 * base_x)
            y_atual = (t_inv**2 * topo_y) + (2 * t_inv * t * ctrl_esq_y) + (t**2 * base_y)

            pontos_gota.append((int(x_atual), int(y_atual)))

        # 4. Metade Direita da Gota (Calcula da Base subindo até ao Topo)
        # Começamos o range em 1 para não adicionar o ponto da base duas vezes seguidas
        for i in range(1, resolucao + 1):
            t = i / resolucao
            t_inv = 1.0 - t

            # Repare que aqui invertemos: começa na Base e termina no Topo
            x_atual = (t_inv**2 * base_x) + (2 * t_inv * t * ctrl_dir_x) + (t**2 * topo_x)
            y_atual = (t_inv**2 * base_y) + (2 * t_inv * t * ctrl_dir_y) + (t**2 * topo_y)

            pontos_gota.append((int(x_atual), int(y_atual)))

        return pontos_gota

    def draw(self, screen):

        poly = self.gota_poly_points()
        try:
            scanline_fill_polygon(screen, poly, self.color)
            # Desenhar contorno preto
            n = len(poly)
            for i in range(n):
                x0, y0 = poly[i]
                x1, y1 = poly[(i + 1) % n]
                line_bresenham(screen, x0, y0, x1, y1, (0, 0, 0))
        except Exception:
            # fallback simples
            draw_circle_bresenham(screen, int(self.x), int(self.y), self.radius, self.color)

    def on_collect(self, game_state):

        if self.color == game_state.current_color or game_state.star_power:
            game_state.registrar_acerto(10)
        else:
            game_state.perder_vida()