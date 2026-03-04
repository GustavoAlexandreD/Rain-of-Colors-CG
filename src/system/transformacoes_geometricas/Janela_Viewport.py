"""
Implementação de:

- Estrutura de Window (Janela no mundo)
- Estrutura de Viewport (Região na tela)
- Transformação world -> viewport (device)
- Suporte a translação e zoom da janela
"""

# ============================================================
# Estrutura de Window
# ============================================================

class Window:
    """
    Representa a janela no espaço do mundo (world coordinates).
    """

    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = float(xmin)
        self.ymin = float(ymin)
        self.xmax = float(xmax)
        self.ymax = float(ymax)

    @property
    def width(self):
        return self.xmax - self.xmin

    @property
    def height(self):
        return self.ymax - self.ymin

    # ----------------------------
    # Translação da janela (pan)
    # ----------------------------
    def translate(self, tx, ty):
        self.xmin += tx
        self.xmax += tx
        self.ymin += ty
        self.ymax += ty

    # ----------------------------
    # Zoom da janela
    # zoom > 1  -> aproxima
    # zoom < 1  -> afasta
    # ----------------------------
    def zoom(self, factor):
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
    Representa a região da tela (device coordinates).
    """

    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = int(xmin)
        self.ymin = int(ymin)
        self.xmax = int(xmax)
        self.ymax = int(ymax)

    @property
    def width(self):
        return self.xmax - self.xmin

    @property
    def height(self):
        return self.ymax - self.ymin


# ============================================================
# Transformação World -> Viewport
# ============================================================

def world_to_viewport(xw, yw, window, viewport):
    """
    Converte coordenadas do mundo (world)
    para coordenadas da viewport (device/screen).

    Fórmula oficial de mapeamento:
    """

    # Normalização horizontal
    xv = viewport.xmin + (
        (xw - window.xmin) * viewport.width / window.width
    )

    # Inversão do eixo Y (porque tela cresce para baixo)
    yv = viewport.ymin + (
        (window.ymax - yw) * viewport.height / window.height
    )

    return round(xv), round(yv)


# ============================================================
# Transformação de lista de vértices
# ============================================================

def map_vertices_to_viewport(vertices, window, viewport):
    """
    Aplica world_to_viewport em uma lista de vértices.
    """

    return [
        world_to_viewport(x, y, window, viewport)
        for (x, y) in vertices
    ]