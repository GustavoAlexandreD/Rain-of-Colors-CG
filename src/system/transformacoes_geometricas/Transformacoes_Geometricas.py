"""
Módulo de Transformações Geométricas 2D baseadas em Matrizes.

Implementação do pipeline matricial conforme ementa da disciplina,
onde as transformações (Translação, Escala, Rotação) geram matrizes 3x3
que podem ser compostas antes de serem aplicadas aos vértices.
"""

import math

def identidade():
    """Retorna a matriz identidade 3x3."""
    return [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

def multiplica_matrizes(m1, m2):
    """
    Multiplica duas matrizes 3x3 (m1 * m2).
    Usada para compor (concatenar) transformações.
    """
    result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += m1[i][k] * m2[k][j]
    return result

def mat_mult_vec(m, v):
    """
    Multiplica uma matriz 3x3 por um vetor (x, y, 1).
    """
    return (
        m[0][0]*v[0] + m[0][1]*v[1] + m[0][2]*v[2],
        m[1][0]*v[0] + m[1][1]*v[1] + m[1][2]*v[2],
        m[2][0]*v[0] + m[2][1]*v[1] + m[2][2]*v[2]
    )

def apply_transform(vertices, mat):
    """
    Aplica uma matriz de transformação a uma lista de vértices.
    """
    transformed = []
    for x, y in vertices:
        vx, vy, _ = mat_mult_vec(mat, (x, y, 1))
        transformed.append((int(vx), int(vy)))
    return transformed

# ============================================================
# GERADORES DE MATRIZES DE TRANSFORMAÇÃO
# ============================================================

def translacao(tx, ty):
    """Retorna a matriz de translação 2D."""
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]

def escala(sx, sy):
    """Retorna a matriz de escala 2D."""
    return [
        [sx,  0, 0],
        [ 0, sy, 0],
        [ 0,  0, 1]
    ]

def rotacao(angulo_graus):
    """Retorna a matriz de rotação 2D (em torno da origem)."""
    theta = math.radians(angulo_graus)
    c = math.cos(theta)
    s = math.sin(theta)
    return [
        [ c, -s, 0],
        [ s,  c, 0],
        [ 0,  0, 1]
    ]

# ============================================================
# FUNÇÕES DE APOIO (Para manter a compatibilidade com seu código antigo)
# ============================================================

def transladar_vertices(vertices, tx, ty):
    mat = translacao(tx, ty)
    return apply_transform(vertices, mat)

def escalar_vertices_pivot(vertices, sx, sy, pivot=None):
    px, py = pivot if pivot else (0, 0)
    # Composição CORRETA: T(px, py) * S(sx, sy) * T(-px, -py)
    # 1º Move para a origem (-), 2º Escala, 3º Volta para o lugar (+)
    m = identidade()
    m = multiplica_matrizes(translacao(-px, -py), m) # <-- SINAL NEGATIVO PRIMEIRO
    m = multiplica_matrizes(escala(sx, sy), m)
    m = multiplica_matrizes(translacao(px, py), m)   # <-- SINAL POSITIVO POR ÚLTIMO
    return apply_transform(vertices, m)

def rotacionar_vertices_pivot(vertices, angulo_graus, pivot=None):
    px, py = pivot if pivot else (0, 0)
    # Composição CORRETA: T(px, py) * R(theta) * T(-px, -py)
    # 1º Move para a origem (-), 2º Rotaciona, 3º Volta para o lugar (+)
    m = identidade()
    m = multiplica_matrizes(translacao(-px, -py), m)  # <-- SINAL NEGATIVO PRIMEIRO
    m = multiplica_matrizes(rotacao(angulo_graus), m)
    m = multiplica_matrizes(translacao(px, py), m)    # <-- SINAL POSITIVO POR ÚLTIMO
    return apply_transform(vertices, m)