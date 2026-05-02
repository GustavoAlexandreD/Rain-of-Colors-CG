"""
Implementação do Pipeline de Visualização Gráfica 2D.

Mapeamento de Window (Mundo) para Viewport (Tela) utilizando
composição de matrizes de transformação, conforme padrão da disciplina.
"""

from system.transformacoes_geometricas.Transformacoes_Geometricas import (
    identidade, translacao, escala, multiplica_matrizes, mat_mult_vec
)

class Window:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin, self.ymin = float(xmin), float(ymin)
        self.xmax, self.ymax = float(xmax), float(ymax)

    @property
    def width(self): return self.xmax - self.xmin
    @property
    def height(self): return self.ymax - self.ymin

class Viewport:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin, self.ymin = int(xmin), int(ymin)
        self.xmax, self.ymax = int(xmax), int(ymax)

    @property
    def width(self): return self.xmax - self.xmin
    @property
    def height(self): return self.ymax - self.ymin


def calcular_matriz_viewport(window, viewport):
    """
    Gera a matriz M de transformação Window-to-Viewport.
    Composição: M = T(Vxmin, Vymin) * S(sx, sy) * T(-Wxmin, -Wymin)
    """
    sx = viewport.width / window.width
    
    # Como a física do seu jogo já usa o eixo Y crescendo para baixo 
    # (a chuva soma +speed no Y para cair), usamos a escala positiva normal!
    sy = viewport.height / window.height 

    m = identidade()
    # 1. Translada o ponto superior esquerdo da Window para a origem
    m = multiplica_matrizes(translacao(-window.xmin, -window.ymin), m)
    
    # 2. Escala para as proporções físicas (SEM INVERTER O Y)
    m = multiplica_matrizes(escala(sx, sy), m)
    
    # 3. Translada para a posição inicial (topo esquerdo) da Viewport na tela
    m = multiplica_matrizes(translacao(viewport.xmin, viewport.ymin), m)
    
    return m

def world_to_viewport(xw, yw, window, viewport):
    """
    Aplica a matriz calculada a um único ponto.
    (Ideal para uso dinâmico, mas se for desenhar um polígono inteiro, 
    é mais eficiente usar map_vertices_to_viewport).
    """
    m = calcular_matriz_viewport(window, viewport)
    vx, vy, _ = mat_mult_vec(m, (xw, yw, 1))
    return int(vx), int(vy)

def map_vertices_to_viewport(vertices, window, viewport):
    """
    Mapeia uma lista inteira de vértices calculando a Matriz M apenas uma vez.
    Altamente otimizado.
    """
    m = calcular_matriz_viewport(window, viewport)
    transformed = []
    for x, y in vertices:
        vx, vy, _ = mat_mult_vec(m, (x, y, 1))
        transformed.append((int(vx), int(vy)))
    return transformed