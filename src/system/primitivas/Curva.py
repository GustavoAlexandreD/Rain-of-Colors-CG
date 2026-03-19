from .Linha import line_bresenham

def curve_bezier(surface, p0_x, p0_y, p1_x, p1_y, p2_x, p2_y, cor):
    resolucao = 20

    ponto_anterior_x = p0_x
    ponto_anterior_y = p0_y

    for i in range(1, resolucao + 1):
        t = i / resolucao

        t_inv = 1.0 - t

        x_atual = (t_inv**2 * p0_x) + (2 * t_inv * t * p1_x) + (t**2 * p2_x)
        y_atual = (t_inv**2 * p0_y) + (2 * t_inv * t * p1_y) + (t**2 * p2_y)

        line_bresenham(surface, round(ponto_anterior_x), round(ponto_anterior_y), round(x_atual), round(y_atual), cor)

        ponto_anterior_x = x_atual
        ponto_anterior_y = y_atual