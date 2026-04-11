"""
Implementação do Pipeline de Visualização Gráfica 2D.

Contém as estruturas para o Mapeamento de Janela (World) para 
Viewport (Device/Screen). Inclui suporte a translação (pan) e 
escala (zoom) do universo do jogo.
"""

# ============================================================
# Estrutura de Window
# ============================================================

class Window:
    """
    Representa a janela de visualização no espaço do mundo (World Coordinates).
    Define o que deve ser visto dentro do universo infinito do jogo.
    Trabalha com valores de ponto flutuante (float) para maior precisão lógica.
    """

    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = float(xmin)
        self.ymin = float(ymin)
        self.xmax = float(xmax)
        self.ymax = float(ymax)

    @property
    def width(self):
        """Retorna a largura atual da janela no mundo."""
        return self.xmax - self.xmin

    @property
    def height(self):
        """Retorna a altura atual da janela no mundo."""
        return self.ymax - self.ymin

    def translate(self, tx, ty):
        """
        Move a janela pelo mundo (Efeito de Pan/Câmera).
        Desloca todos os limites pela mesma taxa de translação (tx, ty).
        """
        self.xmin += tx
        self.xmax += tx
        self.ymin += ty
        self.ymax += ty

    def zoom(self, factor):
        """
        Aplica zoom na janela alterando sua área de cobertura a partir do centro.
        - factor > 1: Aproxima (Janela diminui, objetos parecem maiores na tela)
        - factor < 1: Afasta (Janela aumenta, objetos parecem menores na tela)
        """
        cx = (self.xmin + self.xmax) / 2
        cy = (self.ymin + self.ymax) / 2

        new_half_width  = (self.width  / 2) / factor
        new_half_height = (self.height / 2) / factor

        self.xmin = cx - new_half_width
        self.xmax = cx + new_half_width
        self.ymin = cy - new_half_height
        self.ymax = cy + new_half_height


# ============================================================
# Estrutura de Viewport
# ============================================================

class Viewport:
    """
    Representa a região física na tela do monitor (Device Coordinates).
    Define ONDE a Window será desenhada.
    Trabalha com valores inteiros (int), pois representa pixels reais na tela.
    """

    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = int(xmin)
        self.ymin = int(ymin)
        self.xmax = int(xmax)
        self.ymax = int(ymax)

    @property
    def width(self):
        """Retorna a largura física da viewport em pixels."""
        return self.xmax - self.xmin

    @property
    def height(self):
        """Retorna a altura física da viewport em pixels."""
        return self.ymax - self.ymin


# ============================================================
# Transformação World -> Viewport
# ============================================================

def world_to_viewport(xw, yw, window, viewport):
    """
    Converte coordenadas lógicas do mundo (xw, yw) para 
    coordenadas físicas da tela (xv, yv).

    Fórmula oficial de mapeamento proporcional:
    Xv = Xv_min + (Xw - Xw_min) * (Viewport_Width / Window_Width)
    Yv = Yv_min + (Yw - Yw_min) * (Viewport_Height / Window_Height)
    
    Nota: No eixo Y, a proporção é geralmente invertida dependendo do sistema
    de coordenadas da API gráfica, pois telas costumam crescer para baixo.
    """

    # Normalização e escala no eixo horizontal (Regra de 3)
    xv = viewport.xmin + (
        (xw - window.xmin) * viewport.width / window.width
    )

    # Inversão e escala no eixo vertical (Porque a tela cresce para baixo no Pygame)
    yv = viewport.ymin + (
        (yw - window.ymin) * viewport.height / window.height
    )

    # Retorna valores arredondados, pois não existem "frações" de pixel no monitor
    return round(xv), round(yv)


# ============================================================
# Transformação de lista de vértices
# ============================================================

def map_vertices_to_viewport(vertices, window, viewport):
    """
    Aplica a transformação World-to-Viewport em lote para uma lista de vértices.
    Muito útil para converter polígonos inteiros de uma vez só.
    """
    return [
        world_to_viewport(x, y, window, viewport)
        for (x, y) in vertices
    ]