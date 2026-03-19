import math
import pygame
from src.game.front_end.Componentes import Background
from src.system.primitivas.Curva import curve_bezier
from src.system.primitivas.Linha import line_bresenham
from src.game.scripts.player.Balde_controller import BaldeController
from src.system.preenchimento_e_textura.Texture_Mapping import scanline_texture_polygon
from src.system.primitivas.SetPixel import set_pixel

class Balde():

    def __init__(self, x, y, height: int = 40, top_width: int = 30, base_width: int = 20):
        self.x = x
        self.y = y
        self.height = height
        self.top_width = top_width
        self.base_width = base_width

        center = x + top_width / 2

        self.points = [
            (x, y + 4),                              # topo esquerdo (leve curva)
            (center, y),                             # topo centro (Bezier)
            (x + top_width, y + 4),                  # topo direito
            (center + base_width / 2, y + height - 2),  # base direita
            (center, y + height),                       # base centro
            (center - base_width / 2, y + height - 2)   # base esquerda
        ]

        self.controller = BaldeController()

    def update(self, input_handler):
        """
        Atualiza posição do objeto (movimento da chuva)
        """
        return self.controller.update(input_handler)

    def draw(self, surface, boundary_color, boundary_thickness: int = 1):
        self.fill(surface)

        if boundary_thickness <= 0:
            boundary_thickness = 1

        for i in range(boundary_thickness):
            curve_bezier(surface, self.points[0][0]-i, self.points[0][1], self.points[1][0], self.points[1][1]-i, self.points[2][0]+i, self.points[2][1], boundary_color)
            line_bresenham(surface, self.points[2][0]+i, self.points[2][1], self.points[3][0]+i, self.points[3][1], boundary_color)
            curve_bezier(surface, self.points[3][0]+i, self.points[3][1], self.points[4][0], self.points[4][1]+i, self.points[5][0]-i, self.points[5][1], boundary_color)
            line_bresenham(surface, self.points[5][0]-i, self.points[5][1], self.points[0][0]-i, self.points[0][1], boundary_color)

    def fill(self, surface):
        texture = pygame.image.load("assets/images/balde.jpeg").convert_alpha()
        tex_w, tex_h = texture.get_size()

        texture_matrix = [
            [texture.get_at((tx, ty)) for ty in range(tex_h)]
            for tx in range(tex_w)
        ]

        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        x_min, x_max = int(min(xs)), int(max(xs))
        y_min, y_max = int(min(ys)), int(max(ys))
        w = max(1, x_max - x_min)
        h = max(1, y_max - y_min)

        for y in range(y_min, y_max + 1):
            inters = []
            n = len(self.points)
            for i in range(n):
                x0, y0 = self.points[i]
                x1, y1 = self.points[(i+1) % n]
                if y0 == y1: continue
                if y < min(y0,y1) or y > max(y0,y1): continue
                x = x0 + (y-y0) * (x1-x0) / (y1-y0)
                inters.append(x)
            inters.sort()

            for j in range(0, len(inters), 2):
                if j+1 >= len(inters): break
                x_start = int(math.ceil(inters[j]))
                x_end   = int(math.floor(inters[j+1]))
                for x in range(x_start, x_end+1):
                    u = int((x - x_min) / w * (tex_w-1))
                    v = int((y - y_min) / h * (tex_h-1))
                    c = texture_matrix[u][v]
                    if c.a > 10:
                        set_pixel(surface, x, y, c)

    def on_collect(self, game_state):
        """
        Define o que acontece quando o jogador pega o objeto
        """
        pass