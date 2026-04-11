"""
Módulo de Rasterização de Curvas (Bézier).
"""
from .Linha import line_bresenham

def curve_bezier(surface, p0_x, p0_y, p1_x, p1_y, p2_x, p2_y, cor):
    """
    Desenha uma Curva de Bézier Quadrática interpolando retas de Bresenham.
    Utiliza 3 Pontos de Controle: Início (p0), Ponto de Curvatura (p1) e Fim (p2).
    
    A Equação Paramétrica (t variando de 0 a 1):
    B(t) = (1-t)^2 * P0 + 2*(1-t)*t * P1 + t^2 * P2
    """
    resolucao = 20 # Número de segmentos de reta que formarão a curva
    ponto_anterior_x, ponto_anterior_y = p0_x, p0_y

    for i in range(1, resolucao + 1):
        t = i / resolucao
        t_inv = 1.0 - t

        # Cálculos de Bézier baseados no fator de peso 't'
        x_atual = (t_inv**2 * p0_x) + (2 * t_inv * t * p1_x) + (t**2 * p2_x)
        y_atual = (t_inv**2 * p0_y) + (2 * t_inv * t * p1_y) + (t**2 * p2_y)

        line_bresenham(surface, round(ponto_anterior_x), round(ponto_anterior_y), round(x_atual), round(y_atual), cor)

        ponto_anterior_x, ponto_anterior_y = x_atual, y_atual