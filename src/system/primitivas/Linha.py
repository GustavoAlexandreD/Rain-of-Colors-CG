from .SetPixel import set_pixel
def line_bresenham(surface, x0, y0, x1, y1, color):
    """
    Desenha uma linha usando o algoritmo de Bresenham.
    Compatível com a função set_pixel fornecida.
    """

    x0, y0 = int(x0), int(y0)
    x1, y1 = int(x1), int(y1)

    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    ystep = 1
    if dy < 0:
        ystep = -1
        dy = -dy

    # Bresenham clássico
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x0
    y = y0

    while x <= x1:
        if steep:
            set_pixel(surface, y, x, color)
        else:
            set_pixel(surface, x, y, color)

        if d <= 0:
            d += incE
        else:
            d += incNE
            y += ystep

        x += 1

def line_dda(surface, x0, y0, x1, y1, color):
    """
    Desenha uma reta usando o algoritmo DDA.
    """

    x0, y0 = float(x0), float(y0)
    x1, y1 = float(x1), float(y1)

    dx = x1 - x0
    dy = y1 - y0

    steps = int(max(abs(dx), abs(dy)))

    if steps == 0:
        set_pixel(surface, x0, y0, color)
        return

    x_inc = dx / steps
    y_inc = dy / steps

    x = x0
    y = y0

    for _ in range(steps + 1):
        set_pixel(surface, round(x), round(y), color)
        x += x_inc
        y += y_inc