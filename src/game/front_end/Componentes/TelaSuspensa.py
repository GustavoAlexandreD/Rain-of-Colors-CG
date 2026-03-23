import pygame

from game.front_end.Componentes.Text import draw_text_centered
from system.primitivas.Linha import line_bresenham
from system.preenchimento_e_textura.Preenchimento import flood_fill, scanline_fill


class TelaSuspensa:

    def __init__(self, surface, center_x, center_y, width, height):

        self.surface = surface

        self.cx = int(center_x)
        self.cy = int(center_y)
        self.width = int(width)
        self.height = int(height)

        # Octágono regular centralizado com aparência de bordas arredondadas
        rx = self.width // 2
        ry = self.height // 2
        a = self.height // 12

        # Pontos do octágono
        self.points = [
            (self.cx - rx + a, self.cy - ry),  # Topo esquerdo
            (self.cx + rx - a, self.cy - ry),  # Topo direito
            (self.cx + rx, self.cy - ry + a),  # Direita superior
            (self.cx + rx, self.cy + ry - a),  # Direita inferior
            (self.cx + rx - a, self.cy + ry),  # Fundo direito
            (self.cx - rx + a, self.cy + ry),  # Fundo esquerdo
            (self.cx - rx, self.cy + ry - a),  # Esquerda inferior
            (self.cx - rx, self.cy - ry + a),  # Esquerda superior
        ]

    # ------------------------------------------------------
    # Centro da tela
    # ------------------------------------------------------

    def get_center(self):
        return self.cx, self.cy

    # ------------------------------------------------------
    # Desenho da borda
    # ------------------------------------------------------

    def draw(self, boundary_color, boundary_thickness: int = 1):

        if boundary_thickness <= 0:
            boundary_thickness = 1

        for i in range(boundary_thickness):
            for j in range(len(self.points)):
                p1 = self.points[j]
                p2 = self.points[(j + 1) % len(self.points)]
                line_bresenham(self.surface, p1[0], p1[1] - i, p2[0], p2[1] - i, boundary_color)

    # ------------------------------------------------------
    # Preenchimento
    # ------------------------------------------------------

    def fill(self, fill_color):

        scanline_fill(self.surface, self.points, fill_color)
