"""
Módulo de Transformações Geométricas 2D (Transformações Afins).

Este módulo implementa operações matemáticas clássicas de Computação Gráfica
para manipular objetos na tela. As operações simulam a multiplicação de 
matrizes de transformação (Translação, Escala e Rotação) diretamente 
sobre as coordenadas dos vértices.

Nota: As funções retornam valores em ponto flutuante (float) para preservar
a precisão matemática durante transformações sucessivas. Cabe ao rasterizador
final (Bresenham/Scanline) arredondar esses valores para inteiros (pixels).
"""

import math

# ============================================================
# TRANSLAÇÃO
# ============================================================

def translacao(vertices, tx, ty):
    """
    Aplica translação em uma lista de vértices.
    
    Matriz de Translação 2D (Coordenadas Homogêneas):
    [ 1  0  tx ]   [ x ]   [ x + tx ]
    [ 0  1  ty ] * [ y ] = [ y + ty ]
    [ 0  0  1  ]   [ 1 ]   [   1    ]

    Args:
        vertices: Lista de tuplas (x, y).
        tx: Fator de deslocamento no eixo X.
        ty: Fator de deslocamento no eixo Y.

    Retorna:
        Nova lista de vértices deslocados.
    """
    return [(x + tx, y + ty) for (x, y) in vertices]


# ============================================================
# ESCALA
# ============================================================

def escala(vertices, sx, sy, pivot=None):
    """
    Aplica escala (redimensionamento) em relação a um ponto pivot.
    
    Matriz de Escala 2D:
    [ sx  0  0 ]
    [  0 sy  0 ]
    [  0  0  1 ]

    A matemática utiliza a composição de 3 transformações quando há um pivot:
    1. Translada o objeto para a origem (-px, -py).
    2. Aplica a matriz de Escala.
    3. Translada o objeto de volta para a posição original (+px, +py).

    Args:
        vertices: Lista de tuplas (x, y).
        sx: Fator de escala no eixo X.
        sy: Fator de escala no eixo Y.
        pivot: Tupla (px, py) do ponto fixo. Se None, escala em relação à origem (0,0).
    """
    if pivot is None:
        px, py = 0, 0
    else:
        px, py = pivot

    novos_vertices = []

    for x, y in vertices:
        # 1. Move para a origem relativa ao pivot
        x_rel = x - px
        y_rel = y - py

        # 2. Aplica o fator de escala
        x_esc = x_rel * sx
        y_esc = y_rel * sy

        # 3. Retorna para a posição original no mundo
        novos_vertices.append((x_esc + px, y_esc + py))

    return novos_vertices


# ============================================================
# ROTAÇÃO
# ============================================================

def rotacao(vertices, angulo_graus, pivot=None):
    """
    Aplica rotação 2D (Trigonometria) em relação a um ponto pivot.
    
    Matriz de Rotação 2D:
    [ cos(θ) -sin(θ)  0 ]
    [ sin(θ)  cos(θ)  0 ]
    [   0       0     1 ]

    Assim como na escala, exige translação para a origem e retorno caso
    a rotação não seja em torno do ponto (0,0) global.

    Args:
        vertices: Lista de tuplas (x, y).
        angulo_graus: Ângulo de rotação em graus (convertido internamente para radianos).
        pivot: Tupla (px, py) do ponto fixo (ex: centro do objeto).
    """
    if pivot is None:
        px, py = 0, 0
    else:
        px, py = pivot

    # A função math.cos e math.sin no Python exigem radianos
    theta = math.radians(angulo_graus)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    novos_vertices = []

    for x, y in vertices:
        # 1. Move para a origem relativa ao pivot
        x_rel = x - px
        y_rel = y - py

        # 2. Aplica a Matriz de Rotação 2D
        x_rot = (x_rel * cos_t) - (y_rel * sin_t)
        y_rot = (x_rel * sin_t) + (y_rel * cos_t)

        # 3. Retorna para o sistema de coordenadas original
        novos_vertices.append((x_rot + px, y_rot + py))

    return novos_vertices