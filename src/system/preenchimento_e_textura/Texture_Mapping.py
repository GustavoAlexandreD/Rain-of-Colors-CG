"""
Mapeamento de Textura Afim (Affine Texture Mapping) em Polígonos 2D.

Este módulo é responsável por "encapar" formas geométricas rasterizadas
com imagens reais. Utiliza a abordagem de Scanline (Varredura) combinada
com interpolação linear das coordenadas da textura (U, V).

A otimização é um foco crítico aqui: em vez de consultar a Surface original
(o que é muito lento), o algoritmo acessa diretamente a memória travada da tela
(PixelArray) e lê as cores de uma Matriz de Textura pré-cacheada.
"""

from system.primitivas.SetPixel import set_pixel

# ============================================================
# Rasterizador de Textura
# ============================================================

def scanline_texture_polygon(
    pixel_array,
    screen_w,
    screen_h,
    vertices_uv,
    texture_matrix,
    tex_w,
    tex_h,
    method="standard",
):
    """
    Renderiza um polígono texturizado utilizando interpolação em dois eixos.

    A matemática (Mapeamento Afim):
    1. Interpolação Vertical: Encontra o U e V exatos nas bordas esquerda e direita da linha.
    2. Interpolação Horizontal: Calcula a taxa de variação (Slope/Step) do U e V por pixel.

    Args:
        pixel_array: PixelArrayClone que funciona como o pygame.PixelArray da tela (Buffer de vídeo destravado).
        screen_w, screen_h: Dimensões da tela para recorte (Clipping).
        vertices_uv: Lista de vértices no formato (X_tela, Y_tela, U_textura, V_textura).
                     NOTA: U e V aqui são absolutos (0 a tex_w), não normalizados!
        texture_matrix: Matriz bidimensional cacheada com as cores da imagem original.
        tex_w, tex_h: Dimensões (Largura e Altura) da textura original.
        method: 'standard' (prende a textura na borda) ou 'tiling' (repete a textura).
    """
    
    # Extrai coordenadas Y para definir o alcance do scanline
    y_values = [v[1] for v in vertices_uv]
    y_min = max(0, int(min(y_values)))
    y_max = min(screen_h, int(max(y_values)))

    # Pré-cálculo de limites da textura para evitar processamento dentro do laço
    tex_w_max = tex_w - 1
    tex_h_max = tex_h - 1
    n = len(vertices_uv)

    for y in range(y_min, y_max):
        intersecoes = []
        
        for i in range(n):
            x0, y0, u0, v0 = vertices_uv[i]
            x1, y1, u1, v1 = vertices_uv[(i + 1) % n]

            # Ignora arestas perfeitamente horizontais
            if int(y0) == int(y1):
                continue

            # Garante que a varredura desce (y0 < y1)
            if y0 > y1:
                x0, y0, u0, v0, x1, y1, u1, v1 = x1, y1, u1, v1, x0, y0, u0, v0

            # Verifica se a scanline Y cruza a aresta atual
            if y < y0 or y >= y1:
                continue

            # 1. INTERPOLAÇÃO VERTICAL
            # Calcula a proporção 't' da distância percorrida na aresta
            t = (y - y0) / (y1 - y0)
            
            # Descobre o X na tela e o UV na foto referentes a essa interseção
            x = x0 + (x1 - x0) * t
            u = u0 + (u1 - u0) * t
            v = v0 + (v1 - v0) * t

            intersecoes.append((x, u, v))

        # Ordena as interseções pelo eixo X (da esquerda para a direita)
        intersecoes.sort(key=lambda k: k[0])

        # Preenche os pixels da tela contidos entre os pares de interseção
        for i in range(0, len(intersecoes), 2):
            if i + 1 >= len(intersecoes):
                break

            x_start_f, u_start, v_start = intersecoes[i]
            x_end_f, u_end, v_end = intersecoes[i + 1]

            x_start = int(x_start_f)
            x_end = int(x_end_f)

            span_width = x_end - x_start
            if span_width <= 0:
                continue

            # 2. INTERPOLAÇÃO HORIZONTAL (OTIMIZAÇÃO DE PASSO)
            # Em vez de calcular o 't' para cada pixel, calculamos o incremento
            # exato que o U e o V sofrem ao andar 1 pixel para o lado.
            inv_span = 1.0 / span_width
            u_step = (u_end - u_start) * inv_span
            v_step = (v_end - v_start) * inv_span

            # Recorte (Clipping) contra os limites da tela do monitor
            x_draw_start = max(0, x_start)
            x_draw_end = min(screen_w, x_end)

            # Ajuste de Textura: Se o X_start estava fora da tela (negativo) e foi "puxado"
            # para o 0, temos que avançar o U e V o mesmo número de passos!
            start_skip = x_draw_start - x_start
            cur_u = u_start + (u_step * start_skip)
            cur_v = v_start + (v_step * start_skip)

            # ========================================================
            # DESENHO NA MEMÓRIA DA TELA (Laços separados por Método)
            # ========================================================
            if method == "tiling":
                
                # Método TILING: O UV recomeça ao atingir o limite (Efeito Mosaico)
                for x in range(x_draw_start, x_draw_end):
                    u_int = int(cur_u) % tex_w
                    v_int = int(cur_v) % tex_h

                    color = texture_matrix[u_int][v_int]
                    
                    # Desenha a cor protegendo contra falhas de canal Alpha (RGB vs RGBA)
                    if len(color) < 4 or color[3] >= 10:
                        pixel_array[x, y] = color

                    cur_u += u_step
                    cur_v += v_step
            else:
                
                # Método STANDARD: O UV é "Clampado" nas bordas
                for x in range(x_draw_start, x_draw_end):
                    u_int = int(cur_u)
                    v_int = int(cur_v)

                    # Clamp manual (mais rápido que min/max do Python)
                    if u_int < 0:
                        u_int = 0
                    elif u_int > tex_w_max:
                        u_int = tex_w_max

                    if v_int < 0:
                        v_int = 0
                    elif v_int > tex_h_max:
                        v_int = tex_h_max

                    color = texture_matrix[u_int][v_int]
                    
                    if len(color) < 4 or color[3] >= 10:
                        pixel_array[x, y] = color

                    cur_u += u_step
                    cur_v += v_step