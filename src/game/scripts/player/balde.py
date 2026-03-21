from src.system.primitivas.Linha import line_bresenham
from src.game.scripts.player.Balde_controller import BaldeController
from system.preenchimento_e_textura.Preenchimento import scanline_fill

class Balde():

    def __init__(self, x, y, height: int = 100, top_width: int = 70, base_width: int = 60):
        self.x = x
        self.y = y
        self.controller = BaldeController()
        self.set_size(height, top_width, base_width)

    def _rebuild_points(self):
        center = self.x + self.top_width // 2

        self.points = [
            (self.x, self.y + self.base_width // 3),
            # (center, self.y),
            (self.x + self.top_width, self.y + self.base_width // 3),
            (center + self.base_width // 2, self.y + self.height - self.base_width // 4),
            # (center, self.y + self.height),
            (center - self.base_width // 2, self.y + self.height - self.base_width // 4),
        ]

    def set_size(self, height: int, top_width: int, base_width: int):
        self.height = height
        self.top_width = top_width
        self.base_width = base_width
        self._rebuild_points()

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self._rebuild_points()

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
            line_bresenham(surface, self.points[0][0]-i, self.points[0][1]+i, self.points[1][0]+i, self.points[1][1]+i, boundary_color)
            line_bresenham(surface, self.points[1][0]+i, self.points[1][1]+i, self.points[2][0]+i, self.points[2][1]-i, boundary_color)
            line_bresenham(surface, self.points[2][0]+i, self.points[2][1]-i, self.points[3][0]-i, self.points[3][1]-i, boundary_color)
            line_bresenham(surface, self.points[3][0]-i, self.points[3][1]-i, self.points[0][0]-i, self.points[0][1]+i, boundary_color)

    def fill(self, surface):
        scanline_fill(surface, self.points, (139,69,19))

    def on_collect(self, game_state):
        """
        Define o que acontece quando o jogador pega o objeto
        """
        pass