"""
Módulo de Algoritmos de Preenchimento de Regiões.

Contém as implementações manuais de algoritmos clássicos de Computação Gráfica
para colorir áreas fechadas e polígonos, incluindo Flood Fill, Boundary Fill
e o algoritmo de Varredura (Scanline), além de suporte a sombreamento de Gouraud (Gradientes).
"""

from collections import deque
from system.primitivas.SetPixel import set_pixel

# ============================================================
# Algoritmos de Preenchimento de Vizinhança
# ============================================================

def flood_fill(surface, x, y, fill_color):
    """
    Preenche uma área fechada utilizando o algoritmo Flood Fill (4-conectado).
    
    Utiliza uma abordagem iterativa com Pilha (DFS - Depth First Search) via 'deque' 
    para evitar o limite de recursão nativo do Python (StackOverflow) em áreas muito grandes.
    O preenchimento ocorre substituindo a cor alvo contígua pela nova cor.
    """
    x, y = int(x), int(y)
    width, height = surface.get_size()

    # Validação de limites da tela
    if not (0 <= x < width and 0 <= y < height):
        return

    target_color = surface.get_at((x, y))

    # Se a cor já for a de preenchimento, ignora para evitar loop infinito
    if target_color == fill_color:
        return

    stack = deque()
    stack.append((x, y))

    while stack:
        px, py = stack.pop()

        if not (0 <= px < width and 0 <= py < height):
            continue

        current_color = surface.get_at((px, py))

        if current_color != target_color:
            continue

        set_pixel(surface, px, py, fill_color)

        # Adiciona os 4 vizinhos (Cima, Baixo, Esquerda, Direita) à pilha
        stack.append((px + 1, py))
        stack.append((px - 1, py))
        stack.append((px, py + 1))
        stack.append((px, py - 1))


def boundary_fill(surface, x, y, fill_color, boundary_color):
    """
    Preenche uma região até encontrar uma cor de borda específica (Boundary Fill 4-conectado).
    Também implementado de forma iterativa (Pilha) por questões de performance e segurança de memória.
    """
    x, y = int(x), int(y)
    width, height = surface.get_size()

    if not (0 <= x < width and 0 <= y < height):
        return

    stack = deque()
    stack.append((x, y))

    while stack:
        px, py = stack.pop()

        if not (0 <= px < width and 0 <= py < height):
            continue

        current_color = surface.get_at((px, py))

        # Para se bater na fronteira ou se o pixel já foi pintado com a cor de preenchimento
        if current_color == boundary_color or current_color == fill_color:
            continue

        set_pixel(surface, px, py, fill_color)

        stack.append((px + 1, py))
        stack.append((px - 1, py))
        stack.append((px, py + 1))
        stack.append((px, py - 1))


# ============================================================
# Algoritmos de Varredura (Scanline)
# ============================================================

def scanline_fill(surface, polygon, fill_color):
    """
    Função Wrapper (Alias) para manter compatibilidade com arquivos que
    importam 'scanline_fill'. Redireciona a lógica para o algoritmo otimizado,
    respeitando o princípio DRY (Don't Repeat Yourself).
    """
    scanline_fill_polygon(surface, polygon, fill_color)


def scanline_fill_polygon(surface, vertices, fill_color):
    """
    Preenchimento de polígono usando o algoritmo Scanline (Linha de Varredura).
    
    A matemática do algoritmo:
    1. Encontra os limites verticais (Y-min e Y-max) do polígono.
    2. Para cada linha horizontal (Y), calcula a interseção com as arestas ativas.
    3. Ordena os pontos de interseção (X) da esquerda para a direita.
    4. Pinta os pixels entre os pares de interseção (Regra de paridade ímpar-par).
    """
    if len(vertices) < 3:
        return

    ymin = int(min(y for _, y in vertices))
    ymax = int(max(y for _, y in vertices))

    for y in range(ymin, ymax + 1):
        intersections = []

        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]

            # Ignora arestas perfeitamente horizontais
            if y1 == y2:
                continue

            # Verifica se a scanline Y cruza a aresta atual
            if (y >= min(y1, y2)) and (y < max(y1, y2)):
                # Equação da reta para descobrir o X da interseção
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                intersections.append(x)

        intersections.sort()

        # Preenche os pixels entre cada par de interseções (Início -> Fim)
        for i in range(0, len(intersections), 2):
            if i + 1 >= len(intersections):
                break

            x_start = int(round(intersections[i]))
            x_end   = int(round(intersections[i + 1]))

            for x in range(x_start, x_end + 1):
                set_pixel(surface, x, y, fill_color)

def interpola_cor(c1, c2, t):
    r = int(c1[0] + (c2[0]-c1[0])*t)
    g = int(c1[1] + (c2[1]-c1[1])*t)
    b = int(c1[2] + (c2[2]-c1[2])*t)

    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    
    return (r, g, b)

def scanline_fill_gradient(surface, vertices, colors, a: float|None = None):
    """
    Preenchimento de polígono com sombreamento 2D de Gouraud (Gouraud Shading).
    
    Interpola linearmente as cores dos vértices em duas etapas:
    1. Interpolação Vertical: Calcula as cores nas bordas (interseções das arestas).
    2. Interpolação Horizontal: Calcula o gradiente pixel a pixel entre os limites da scanline.
    """
    if len(vertices) < 3:
        return

    if len(vertices) != len(colors):
        raise ValueError("A quantidade de vértices e cores deve ser exatamente a mesma.")

    ys = [p[1] for p in vertices]
    y_min = int(min(ys))
    y_max = int(max(ys))

    n = len(vertices)

    for y in range(y_min, y_max):
        intersections = []

        for i in range(n):
            x0, y0 = vertices[i]
            x1, y1 = vertices[(i + 1) % n]

            c0 = colors[i]
            c1 = colors[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                c0, c1 = c1, c0

            if y < y0 or y >= y1:
                continue

            ty = (y - y0)*a / (y1 - y0)
            tx = (y - y0) / (y1 - y0)
            x = x0 + tx*(x1 - x0)
            cor_y = interpola_cor(c0, c1, ty)

            intersections.append((x, cor_y))

        intersections.sort(key=lambda i: i[0])

        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                x_ini, cor_ini = intersections[i]
                x_fim, cor_fim = intersections[i + 1]

                if x_fim == x_ini:
                    continue

                for x in range(int(x_ini), int(x_fim) + 1):
                    t = (x - x_ini) / (x_fim - x_ini)
                    cor = interpola_cor(cor_ini, cor_fim, t)
                    set_pixel(surface, x, y, cor)