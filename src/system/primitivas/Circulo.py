from .SetPixel import set_pixel
def draw_circle_bresenham(surface, cx, cy, radius, color):
    """
    Desenha um círculo usando o algoritmo de Bresenham (Midpoint).
    cx, cy -> centro
    radius -> raio
    """

    x = 0
    y = radius
    d = 1 - radius  # parâmetro de decisão inicial

    while x <= y:

        # 8 pontos simétricos
        set_pixel(surface, cx + x, cy + y, color)
        set_pixel(surface, cx - x, cy + y, color)
        set_pixel(surface, cx + x, cy - y, color)
        set_pixel(surface, cx - x, cy - y, color)
        set_pixel(surface, cx + y, cy + x, color)
        set_pixel(surface, cx - y, cy + x, color)
        set_pixel(surface, cx + y, cy - x, color)
        set_pixel(surface, cx - y, cy - x, color)

        x += 1

        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1