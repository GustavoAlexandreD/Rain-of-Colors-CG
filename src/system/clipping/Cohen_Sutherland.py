from system.primitivas.Linha import line_bresenham

"""
Implementação do algoritmo de recorte de linhas de Cohen–Sutherland.
"""

# =============================
# Códigos de Região (Outcodes)
# =============================

INSIDE = 0
LEFT   = 1
RIGHT  = 2
BOTTOM = 4
TOP    = 8


# =============================
# Função para calcular outcode
# =============================

def compute_outcode(x, y, xmin, ymin, xmax, ymax):
    """
    Calcula o código de região (outcode) para um ponto.
    """

    code = INSIDE

    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT

    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP

    return code


# =============================
# Algoritmo Principal
# =============================

def cohen_sutherland_clip(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    """
    Executa o recorte de linha usando Cohen–Sutherland.

    Retorna:
        (x0, y0, x1, y1) recortados se a linha for visível
        None se estiver totalmente fora
    """

    outcode0 = compute_outcode(x0, y0, xmin, ymin, xmax, ymax)
    outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)

    while True:

        # Caso 1: completamente dentro
        if not (outcode0 | outcode1):
            return (
                round(x0),
                round(y0),
                round(x1),
                round(y1),
            )

        # Caso 2: completamente fora
        if outcode0 & outcode1:
            return None

        # Caso 3: parcialmente visível
        outcode_out = outcode0 if outcode0 != 0 else outcode1

        # Interseção com bordas
        if outcode_out & TOP:
            # y = ymax
            if y1 != y0:
                x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
            else:
                x = x0
            y = ymax

        elif outcode_out & BOTTOM:
            # y = ymin
            if y1 != y0:
                x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
            else:
                x = x0
            y = ymin

        elif outcode_out & RIGHT:
            # x = xmax
            if x1 != x0:
                y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
            else:
                y = y0
            x = xmax

        elif outcode_out & LEFT:
            # x = xmin
            if x1 != x0:
                y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
            else:
                y = y0
            x = xmin

        # Atualiza ponto externo
        if outcode_out == outcode0:
            x0, y0 = x, y
            outcode0 = compute_outcode(x0, y0, xmin, ymin, xmax, ymax)
        else:
            x1, y1 = x, y
            outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)


# =============================
# Função Integrada com Bresenham
# =============================

def draw_clipped_line(surface, x0, y0, x1, y1,
                      xmin, ymin, xmax, ymax,
                      color):
    """
    Recorta a linha usando Cohen–Sutherland e,
    se visível, desenha com line_bresenham.
    """

    result = cohen_sutherland_clip(
        x0, y0, x1, y1,
        xmin, ymin, xmax, ymax
    )

    if result:
        x0, y0, x1, y1 = result
        line_bresenham(surface, x0, y0, x1, y1, color)