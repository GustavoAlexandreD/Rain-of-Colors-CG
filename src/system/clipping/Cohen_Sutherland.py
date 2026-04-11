from system.primitivas.Linha import line_bresenham

"""
Implementação do algoritmo de recorte (Clipping) analítico de Cohen-Sutherland.
Utilizado para descartar partes de linhas que caem fora de uma área visível (Viewport),
otimizando a renderização gráfica.
"""

# =============================
# Códigos de Região (Outcodes)
# =============================
# Representação binária para as 9 áreas ao redor da tela (Top, Bottom, Right, Left)
INSIDE = 0  # 0000
LEFT   = 1  # 0001
RIGHT  = 2  # 0010
BOTTOM = 4  # 0100
TOP    = 8  # 1000

def compute_outcode(x, y, xmin, ymin, xmax, ymax):
    """
    Calcula o código de região (Outcode) binário para um ponto (x, y).
    Utiliza operadores bitwise (OR '|' ) para ligar os bits correspondentes.
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

def cohen_sutherland_clip(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    """
    Avalia e recorta uma linha usando Cohen-Sutherland.

    Retorna:
        - Uma tupla (x0, y0, x1, y1) com os novos pontos, se a linha for visível.
        - None, se a linha for trivialmente rejeitada (completamente fora).
    """
    outcode0 = compute_outcode(x0, y0, xmin, ymin, xmax, ymax)
    outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)

    while True:
        # Trivialmente Aceito: Ambos os pontos estão dentro da tela (0000)
        if not (outcode0 | outcode1):
            return round(x0), round(y0), round(x1), round(y1)

        # Trivialmente Rejeitado: Ambos os pontos partilham a mesma zona fora da tela
        if outcode0 & outcode1:
            return None

        # A linha cruza a borda. Descobre qual ponto está fora para recortá-lo
        outcode_out = outcode0 if outcode0 != 0 else outcode1

        # Interseção com as bordas usando a equação da reta: y = mx + b
        if outcode_out & TOP:
            x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0) if y1 != y0 else x0
            y = ymax
        elif outcode_out & BOTTOM:
            x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0) if y1 != y0 else x0
            y = ymin
        elif outcode_out & RIGHT:
            y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0) if x1 != x0 else y0
            x = xmax
        elif outcode_out & LEFT:
            y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0) if x1 != x0 else y0
            x = xmin

        # Substitui o ponto de fora pelo ponto de interseção recém calculado
        if outcode_out == outcode0:
            x0, y0 = x, y
            outcode0 = compute_outcode(x0, y0, xmin, ymin, xmax, ymax)
        else:
            x1, y1 = x, y
            outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)

def draw_clipped_line(surface, x0, y0, x1, y1, xmin, ymin, xmax, ymax, color):
    """Aplica o clipping na linha e a desenha via Bresenham apenas se for visível."""
    result = cohen_sutherland_clip(x0, y0, x1, y1, xmin, ymin, xmax, ymax)
    if result:
        x_clipped0, y_clipped0, x_clipped1, y_clipped1 = result
        line_bresenham(surface, x_clipped0, y_clipped0, x_clipped1, y_clipped1, color)