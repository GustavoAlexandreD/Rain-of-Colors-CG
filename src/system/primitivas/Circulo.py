from .SetPixel import set_pixel


def _draw_hline(surface, x_start, x_end, y, color):
    if y < 0 or y >= surface.get_height():
        return

    if x_start > x_end:
        x_start, x_end = x_end, x_start

    width = surface.get_width()
    x0 = max(0, x_start)
    x1 = min(width - 1, x_end)

    for x in range(x0, x1 + 1):
        set_pixel(surface, x, y, color)


def draw_circle_bresenham(surface, cx, cy, radius, color, boundary_thickness: int = 1):
    """
    Desenha um círculo usando o algoritmo de Bresenham (Midpoint).
    cx, cy -> centro
    radius -> raio
    color -> cor da borda
    boundary_thickness -> espessura da borda
    """
    if boundary_thickness <= 0:
        boundary_thickness = 1

    vertices = []
    x = 0
    y = radius 
    d = 1 - radius  # parâmetro de decisão inicial

    while x <= y:
        # 8 pontos simétricos
        for i in range(boundary_thickness):
            y_temp = y + i
            set_pixel(surface, cx + x, cy + y_temp, color)
            set_pixel(surface, cx - x, cy + y_temp, color)
            set_pixel(surface, cx + x, cy - y_temp, color)
            set_pixel(surface, cx - x, cy - y_temp, color)
            set_pixel(surface, cx + y_temp, cy + x, color)
            set_pixel(surface, cx - y_temp, cy + x, color)
            set_pixel(surface, cx + y_temp, cy - x, color)
            set_pixel(surface, cx - y_temp, cy - x, color)
            if i == 0:
                vertices.append((cx + x, cy + y))
                vertices.append((cx - x, cy + y))
                vertices.append((cx + x, cy - y))
                vertices.append((cx - x, cy - y))
                vertices.append((cx + y, cy + x))
                vertices.append((cx - y, cy + x))
                vertices.append((cx + y, cy - x))
                vertices.append((cx - y, cy - x))

        x += 1

        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1

    return vertices


def draw_filled_circle_bresenham(surface, cx, cy, radius, fill_color, boundary_color=None, boundary_thickness: int = 1):
    """
    Desenha e preenche um círculo usando variantes do algoritmo de Bresenham.
    """
    if radius < 0:
        return

    x = 0
    y = radius
    d = 1 - radius

    while x <= y:
        _draw_hline(surface, cx - x, cx + x, cy + y, fill_color)
        _draw_hline(surface, cx - x, cx + x, cy - y, fill_color)
        _draw_hline(surface, cx - y, cx + y, cy + x, fill_color)
        _draw_hline(surface, cx - y, cx + y, cy - x, fill_color)

        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1

    if boundary_color is not None and boundary_thickness > 0:
        draw_circle_bresenham(surface, cx, cy, radius, boundary_color, boundary_thickness)
