from src.system.primitivas.Curva import curve_bezier
from src.system.primitivas.Linha import line_bresenham
from src.game.front_end.Componentes.Background import Background

class Balde():

    def __init__(self, x, y, height: int = 40, top_width: int = 30, base_width: int = 20):
        self.x = x
        self.y = y
        self.height = height
        self.top_width = top_width
        self.base_width = base_width
        self.active = True

        center = x + top_width / 2

        self.points = [
            (x, y + 4),                              # topo esquerdo (leve curva)
            (center, y),                             # topo centro (Bezier)
            (x + top_width, y + 4),                  # topo direito
            (center + base_width / 2, y + height - 2),  # base direita
            (center, y + height),                       # base centro
            (center - base_width / 2, y + height - 2)   # base esquerda
        ]

    def update(self):
        """
        Atualiza posição do objeto (movimento da chuva)
        """
        self.y += self.speed

    def draw(self, surface, boundary_color, boundary_thickness: int = 1):
        if boundary_thickness <= 0:
            boundary_thickness = 1

        for i in range(boundary_thickness):
            curve_bezier(surface, self.points[0][0]-i, self.points[0][1], self.points[1][0], self.points[1][1]-i, self.points[2][0]+i, self.points[2][1], boundary_color)
            line_bresenham(surface, self.points[2][0]+i, self.points[2][1], self.points[3][0]+i, self.points[3][1], boundary_color)
            curve_bezier(surface, self.points[3][0]+i, self.points[3][1], self.points[4][0], self.points[4][1]+i, self.points[5][0]-i, self.points[5][1], boundary_color)
            line_bresenham(surface, self.points[5][0]-i, self.points[5][1], self.points[0][0]-i, self.points[0][1], boundary_color)

    def fill(self, surface):
        Background(self.base_width, self.height, "assets/images/balde.jpeg").render_once()

    def on_collect(self, game_state):
        """
        Define o que acontece quando o jogador pega o objeto
        """
        pass