from system.primitivas.Circulo import draw_circle_bresenham
from system.primitivas.Linha import line_bresenham
from system.preenchimento_e_textura.Preenchimento import flood_fill


class Coracoes:
    """Componente de UI que desenha até 3 corações na tela.

    Usa apenas as primitivas do pacote `system` (sem pygame direto).
    """

    def __init__(self, surface, pos=(10, 10), spacing=40, size=32, color=(220, 20, 60)):
        self.surface = surface
        self.x, self.y = pos
        self.spacing = spacing
        self.size = size
        self.color = color
        self.off_color = (60, 60, 60)
        self.max_lives = 3
        self.lives = self.max_lives

    def apagar(self):
        """Apaga (desliga) o último coração visível.

        Decrementa o contador interno e redesenha os corações.
        """
        if self.lives <= 0:
            return
        self.lives -= 1
        self.draw()

    def reset(self):
        self.lives = self.max_lives
        self.draw()

    def draw(self):
        """Desenha todos os corações na superfície atualizando seu estado."""
        for i in range(self.max_lives):
            cx = self.x + i * self.spacing
            cy = self.y
            on = i < self.lives
            self._draw_heart(cx, cy, self.size, self.color if on else self.off_color)

    def _draw_heart(self, cx, cy, size, color):
        """Desenha um coração aproximado usando duas circunferências + triângulo e preenche.

        Parâmetros: cx,cy centro do coração (parte superior), size largura aproximada.
        """
        # parâmetros relativos
        r = max(2, int(size * 0.28))

        # centros das duas 'bolinhas' superiores
        left_cx = cx - r
        right_cx = cx + r
        top_cy = cy - int(r * 0.2)

        # ponto inferior do coração
        bottom_x = cx
        bottom_y = cy + int(size * 0.45)

        # desenha contorno: duas circunferências e linhas para formar a ponta
        draw_circle_bresenham(self.surface, left_cx, top_cy, r, color)
        draw_circle_bresenham(self.surface, right_cx, top_cy, r, color)

        # linhas laterais convergindo para a ponta
        line_bresenham(self.surface, left_cx - r, cy, bottom_x, bottom_y, color)
        line_bresenham(self.surface, right_cx + r, cy, bottom_x, bottom_y, color)

        # garante topo fechado aproximando entre as duas circunferências
        line_bresenham(self.surface, left_cx - r, cy, right_cx + r, cy, color)

        # preenche o interior usando flood fill a partir de um ponto interno
        seed_x = cx
        seed_y = cy + int(size * 0.05)
        try:
            flood_fill(self.surface, seed_x, seed_y, color)
        except Exception:
            # se o flood_fill falhar por qualquer razão, apenas ignore
            pass
