from typing import Optional

from src.system.primitivas.Linha import line_bresenham
from src.system.preenchimento_e_textura.Preenchimento import flood_fill, scanline_fill


class Button:

    def __init__(self, surface, x, y, width, height, text: Optional[str] = None):

        self.surface = surface

        self.x = int(x)
        self.y = int(y)

        self.width = int(width)
        self.height = int(height)

        self.text = text

        self.points = [
            (self.x + 3, self.y),
            (self.x + (self.width - 6), self.y),
            (self.x + (self.width - 3), self.y + 4),
            (self.x + (self.width - 3), self.y + (self.height - 8)),
            (self.x + (self.width - 6), self.y + (self.height - 4)),
            (self.x + 3, self.y + (self.height - 4)),
            (self.x, self.y + (self.height - 8)),
            (self.x, self.y + 4),
        ]

    # ------------------------------------------------------
    # Centro do botão
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

        cx,cy = self.get_center()
        scanline_fill(self.surface, self.points, (0,0,0))
        flood_fill(self.surface, cx, cy, fill_color)