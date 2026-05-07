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
        
        # Guardar os limites iniciais (As paredes do mundo original)
        self.limit_xmin = self.xmin
        self.limit_ymin = self.ymin
        self.limit_xmax = self.xmax
        self.limit_ymax = self.ymax

    @property
    def width(self): return self.xmax - self.xmin
    @property
    def height(self): return self.ymax - self.ymin

    def translate(self, tx, ty):
        """
        Move a janela limitando o movimento às bordas do mundo original.
        """
        # 1. Verifica se vai bater nos limites horizontais (Esquerda/Direita)
        if self.xmin + tx < self.limit_xmin:
            tx = self.limit_xmin - self.xmin  # Trava na esquerda
        elif self.xmax + tx > self.limit_xmax:
            tx = self.limit_xmax - self.xmax  # Trava na direita

        # 2. Verifica se vai bater nos limites verticais (Cima/Baixo)
        if self.ymin + ty < self.limit_ymin:
            ty = self.limit_ymin - self.ymin  # Trava no teto
        elif self.ymax + ty > self.limit_ymax:
            ty = self.limit_ymax - self.ymax  # Trava no chão

        # 3. Aplica apenas o movimento permitido
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
        """
        Aumenta ou diminui a área de visão a partir do centro.
        """
        cx, cy = (self.xmin + self.xmax) / 2, (self.ymin + self.ymax) / 2
        
        nova_largura = self.width / factor
        nova_altura = self.height / factor
        
        self.xmin = cx - nova_largura / 2
        self.xmax = cx + nova_largura / 2
        self.ymin = cy - nova_altura / 2
        self.ymax = cy + nova_altura / 2

        # ==========================================
        # TRAVA DE SEGURANÇA (CLAMPING)
        # ==========================================
        if self.xmin < self.limit_xmin:
            shift = self.limit_xmin - self.xmin
            self.xmin += shift
            self.xmax += shift
            
        if self.xmax > self.limit_xmax:
            shift = self.xmax - self.limit_xmax
            self.xmin -= shift
            self.xmax -= shift

        if self.ymin < self.limit_ymin:
            shift = self.limit_ymin - self.ymin
            self.ymin += shift
            self.ymax += shift
            
        if self.ymax > self.limit_ymax:
            shift = self.ymax - self.limit_ymax
            self.ymin -= shift
            self.ymax -= shift

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