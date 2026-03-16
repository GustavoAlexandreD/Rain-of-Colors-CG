from typing import Optional

import pygame
import os

from src.system.primitivas.Linha import line_bresenham
from src.system.primitivas.Circulo import draw_circle_bresenham
from src.system.primitivas.Elipse import ellipse_bresenham
from src.system.preenchimento_e_textura.Preenchimento import scanline_fill
from src.system.preenchimento_e_textura.Preenchimento import scanline_fill_polygon
from src.system.preenchimento_e_textura.Texture_Mapping import scanline_texture_polygon

class Button:
    def __init__(self,surface, x, y, width, height, text: Optional[str] = None):
        self.surface = surface
        x, y = int(x), int(y)
        width, height = int(width), int(height)
        self.text = text
        self.points = [(x +3, y),
                       (x + (width-6), y),
                       (x + (width-3), y + 4),
                       (x + (width-3), y + (height-8)),
                       (x + (width-6), y + (height-4)),
                       (x + 3, y + (height-4)),
                       (x, y + (height-8)),
                       (x , y + 4)]
    
    def draw(self, boundary_color, boundary_thickness: int = 1):
        if boundary_thickness <=0:
            boundary_thickness = 1
        for i in range(boundary_thickness):
            line_bresenham(self.surface, self.points[0][0], self.points[0][1]-i, self.points[1][0], self.points[1][1]-i, boundary_color)
            line_bresenham(self.surface, self.points[1][0], self.points[1][1]-i, self.points[2][0]+i, self.points[2][1], boundary_color)
            line_bresenham(self.surface, self.points[2][0]+i, self.points[2][1], self.points[3][0]+i, self.points[3][1], boundary_color)
            line_bresenham(self.surface, self.points[3][0]+i, self.points[3][1], self.points[4][0], self.points[4][1]+i, boundary_color)
            line_bresenham(self.surface, self.points[4][0], self.points[4][1]+i, self.points[5][0], self.points[5][1]+i, boundary_color)
            line_bresenham(self.surface, self.points[5][0], self.points[5][1]+i, self.points[6][0]-i, self.points[6][1], boundary_color)
            line_bresenham(self.surface, self.points[6][0]-i, self.points[6][1], self.points[7][0]-i, self.points[7][1], boundary_color)
            line_bresenham(self.surface, self.points[7][0]-i, self.points[7][1], self.points[0][0], self.points[0][1]+i, boundary_color)
            
    def fill(self, fill_color):
        scanline_fill(self.surface, self.points, fill_color)
