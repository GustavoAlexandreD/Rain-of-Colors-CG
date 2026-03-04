"""
Módulo de Transformações Geométricas 2D
"""

import math


# ============================================================
# TRANSLAÇÃO
# ============================================================

def translacao(vertices, tx, ty):
    """
    Aplica translação em uma lista de vértices.

    vertices -> [(x1, y1), (x2, y2), ...]
    tx -> deslocamento em x
    ty -> deslocamento em y

    Retorna nova lista transformada.
    """

    return [(x + tx, y + ty) for (x, y) in vertices]


# ============================================================
# ESCALA
# ============================================================

def escala(vertices, sx, sy, pivot=None):
    """
    Aplica escala em relação a um ponto pivot.

    vertices -> [(x1, y1), ...]
    sx -> fator de escala em x
    sy -> fator de escala em y
    pivot -> (px, py) opcional. Se None, escala em relação à origem (0,0)
    """

    if pivot is None:
        px, py = 0, 0
    else:
        px, py = pivot

    novos_vertices = []

    for x, y in vertices:
        # Move para origem relativa ao pivot
        x_rel = x - px
        y_rel = y - py

        # Aplica escala
        x_esc = x_rel * sx
        y_esc = y_rel * sy

        # Retorna para posição original
        novos_vertices.append((x_esc + px, y_esc + py))

    return novos_vertices


# ============================================================
# ROTAÇÃO
# ============================================================

def rotacao(vertices, angulo_graus, pivot=None):
    """
    Aplica rotação 2D.

    angulo_graus -> ângulo em graus
    pivot -> (px, py) ponto de rotação
             Se None, rotaciona em torno da origem (0,0)
    """

    if pivot is None:
        px, py = 0, 0
    else:
        px, py = pivot

    theta = math.radians(angulo_graus)

    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    novos_vertices = []

    for x, y in vertices:

        # Move para origem relativa ao pivot
        x_rel = x - px
        y_rel = y - py

        # Matriz de rotação 2D:
        # [ cos -sin ]
        # [ sin  cos ]
        x_rot = x_rel * cos_t - y_rel * sin_t
        y_rot = x_rel * sin_t + y_rel * cos_t

        # Retorna ao sistema original
        novos_vertices.append((x_rot + px, y_rot + py))

    return novos_vertices