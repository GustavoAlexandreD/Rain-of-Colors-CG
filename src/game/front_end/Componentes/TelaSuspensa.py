import pygame

from game.front_end.Componentes.Text import draw_text_centered
from system.primitivas.Linha import line_bresenham
from system.preenchimento_e_textura.Preenchimento import flood_fill, scanline_fill


class TelaSuspensa:

    def __init__(self, surface, center_x, start_y, width, height):

        self.surface = surface

        self.x = center_x-(width//2)
        self.cx = int(center_x)
        self.y = int(start_y)

        self.width = int(width)
        self.height = int(height)
        margin_x = self.x//6
        margin_y = self.y//4

        self.points = [
            (self.x + margin_x//2, self.y),
            (self.x + (self.width - margin_x), self.y),
            (self.x + (self.width - margin_x//2), self.y + margin_y//2),
            (self.x + (self.width - margin_x//2), self.y + (self.height - margin_y)),
            (self.x + (self.width - margin_x), self.y + (self.height - margin_y//2)),
            (self.x + 3, self.y + (self.height - margin_y//2)),
            (self.x, self.y + (self.height - margin_y)),
            (self.x, self.y + margin_y//2),
        ]

    # ------------------------------------------------------
    # Centro da tela
    # ------------------------------------------------------

    def get_center(self):

        cx = self.x + self.width // 2
        cy = self.y + self.height // 2

        return cx, cy

    # ------------------------------------------------------
    # Desenho da borda
    # ------------------------------------------------------

    def draw(self, boundary_color, boundary_thickness: int = 1):

        if boundary_thickness <= 0:
            boundary_thickness = 1

        for i in range(boundary_thickness):

            line_bresenham(self.surface, self.points[0][0], self.points[0][1] - i, self.points[1][0], self.points[1][1] - i, boundary_color)

            line_bresenham(self.surface, self.points[1][0], self.points[1][1] - i, self.points[2][0] + i, self.points[2][1], boundary_color)

            line_bresenham(self.surface, self.points[2][0] + i, self.points[2][1], self.points[3][0] + i, self.points[3][1], boundary_color)

            line_bresenham(self.surface, self.points[3][0] + i, self.points[3][1], self.points[4][0], self.points[4][1] + i, boundary_color)

            line_bresenham(self.surface, self.points[4][0], self.points[4][1] + i, self.points[5][0], self.points[5][1] + i, boundary_color)

            line_bresenham(self.surface, self.points[5][0], self.points[5][1] + i, self.points[6][0] - i, self.points[6][1], boundary_color)

            line_bresenham(self.surface, self.points[6][0] - i, self.points[6][1], self.points[7][0] - i, self.points[7][1], boundary_color)

            line_bresenham(self.surface, self.points[7][0] - i, self.points[7][1], self.points[0][0], self.points[0][1] + i, boundary_color)

    # ------------------------------------------------------
    # Preenchimento
    # ------------------------------------------------------

    def fill(self, fill_color):

        cx, cy = self.get_center()
        scanline_fill(self.surface, self.points, (0,0,0))
        flood_fill(self.surface, cx, cy, fill_color)
