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