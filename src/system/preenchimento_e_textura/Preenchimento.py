from collections import deque
from system.primitivas.SetPixel import set_pixel


# ============================================================
# Flood Fill (4-conectado)
# ============================================================

def flood_fill(surface, x, y, fill_color):
    """
    Preenche uma área usando Flood Fill (4-conectado).
    O preenchimento ocorre enquanto a cor inicial for igual.
    """

    x, y = int(x), int(y)
    width, height = surface.get_size()

    if not (0 <= x < width and 0 <= y < height):
        return

    target_color = surface.get_at((x, y))

    # Se a cor já for a de preenchimento, não faz nada
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

        # 4 vizinhos
        stack.append((px + 1, py))
        stack.append((px - 1, py))
        stack.append((px, py + 1))
        stack.append((px, py - 1))


# ============================================================
# Boundary Fill (4-conectado)
# ============================================================

def boundary_fill(surface, x, y, fill_color, boundary_color):
    """
    Preenche uma área até encontrar a cor de contorno (boundary_color).
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

        if current_color == boundary_color or current_color == fill_color:
            continue

        set_pixel(surface, px, py, fill_color)

        # 4 vizinhos
        stack.append((px + 1, py))
        stack.append((px - 1, py))
        stack.append((px, py + 1))
        stack.append((px, py - 1))


# ============================================================
# Scanline Fill para Polígonos
# ============================================================

def scanline_fill_polygon(surface, vertices, fill_color):
    """
    Preenchimento de polígono usando algoritmo Scanline.

    vertices -> lista de tuplas [(x1,y1), (x2,y2), ...]
    """

    if len(vertices) < 3:
        return

    # Encontrar limites verticais
    ymin = min(y for _, y in vertices)
    ymax = max(y for _, y in vertices)

    ymin = int(ymin)
    ymax = int(ymax)

    # Percorre cada linha horizontal
    for y in range(ymin, ymax + 1):

        intersections = []

        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]

            # Ignora arestas horizontais
            if y1 == y2:
                continue

            # Verifica se a scanline cruza a aresta
            if (y >= min(y1, y2)) and (y < max(y1, y2)):

                # Calcula interseção
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                intersections.append(x)

        # Ordena interseções
        intersections.sort()

        # Preenche entre pares
        for i in range(0, len(intersections), 2):
            if i + 1 >= len(intersections):
                break

            x_start = int(round(intersections[i]))
            x_end   = int(round(intersections[i + 1]))

            for x in range(x_start, x_end + 1):
                set_pixel(surface, x, y, fill_color)

def scanline_fill_polygon_gradient(surface, vertices, colors):
    """
    Preenchimento de polígono com gradiente por vértice (Gouraud 2D).

    vertices -> [(x,y), ...]
    colors   -> [(r,g,b), ...] mesma ordem dos vértices
    """

    if len(vertices) < 3:
        return

    # Garantir mesma quantidade
    if len(vertices) != len(colors):
        raise ValueError("Vertices e colors devem ter o mesmo tamanho")

    # Limites verticais
    ymin = int(min(y for _, y in vertices))
    ymax = int(max(y for _, y in vertices))

    for y in range(ymin, ymax + 1):

        intersections = []

        for i in range(len(vertices)):

            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]

            r1, g1, b1 = colors[i]
            r2, g2, b2 = colors[(i + 1) % len(vertices)]

            # Ignora arestas horizontais
            if y1 == y2:
                continue

            # Verifica se scanline cruza aresta
            if (y >= min(y1, y2)) and (y < max(y1, y2)):

                t = (y - y1) / (y2 - y1)

                # Interpolação da posição
                x = x1 + t * (x2 - x1)

                # Interpolação da cor na aresta
                r = r1 + t * (r2 - r1)
                g = g1 + t * (g2 - g1)
                b = b1 + t * (b2 - b1)

                intersections.append((x, r, g, b))

        # Ordenar por X
        intersections.sort(key=lambda item: item[0])

        # Preencher entre pares
        for i in range(0, len(intersections), 2):

            if i + 1 >= len(intersections):
                break

            x_start, r_start, g_start, b_start = intersections[i]
            x_end,   r_end,   g_end,   b_end   = intersections[i + 1]

            x_start = int(round(x_start))
            x_end   = int(round(x_end))

            dx = x_end - x_start

            if dx == 0:
                continue

            for x in range(x_start, x_end + 1):

                t = (x - x_start) / dx

                # Interpolação horizontal da cor
                r = r_start + t * (r_end - r_start)
                g = g_start + t * (g_end - g_start)
                b = b_start + t * (b_end - b_start)

                # Clamp segurança
                r = max(0, min(int(r), 255))
                g = max(0, min(int(g), 255))
                b = max(0, min(int(b), 255))

                set_pixel(surface, x, y, (r, g, b))