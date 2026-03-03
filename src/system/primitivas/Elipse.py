from .SetPixel import set_pixel
def ellipse_bresenham(surface, cx, cy, a, b, color):
    """
    Desenha uma elipse usando o Midpoint Ellipse Algorithm.
    cx, cy -> centro
    a -> raio horizontal
    b -> raio vertical
    """

    x = 0
    y = b

    a2 = a * a
    b2 = b * b

    # Região 1
    d1 = b2 - a2 * b + 0.25 * a2
    dx = 2 * b2 * x
    dy = 2 * a2 * y

    while dx < dy:

        # 4 pontos simétricos
        set_pixel(surface, cx + x, cy + y, color)
        set_pixel(surface, cx - x, cy + y, color)
        set_pixel(surface, cx + x, cy - y, color)
        set_pixel(surface, cx - x, cy - y, color)

        if d1 < 0:
            x += 1
            dx = 2 * b2 * x
            d1 += dx + b2
        else:
            x += 1
            y -= 1
            dx = 2 * b2 * x
            dy = 2 * a2 * y
            d1 += dx - dy + b2

    # Região 2
    d2 = (
        b2 * (x + 0.5) * (x + 0.5)
        + a2 * (y - 1) * (y - 1)
        - a2 * b2
    )

    while y >= 0:

        set_pixel(surface, cx + x, cy + y, color)
        set_pixel(surface, cx - x, cy + y, color)
        set_pixel(surface, cx + x, cy - y, color)
        set_pixel(surface, cx - x, cy - y, color)

        if d2 > 0:
            y -= 1
            dy = 2 * a2 * y
            d2 += a2 - dy
        else:
            y -= 1
            x += 1
            dx = 2 * b2 * x
            dy = 2 * a2 * y
            d2 += dx - dy + a2