"""
Mapeamento de textura em polígonos 2D usando Scanline + interpolação UV.

Requisitos:
- surface: pygame.Surface destino
- texture: pygame.Surface da imagem
- vertices: [(x,y), ...]
- uvs: [(u,v), ...]  valores normalizados (0 a 1)
"""

from system.primitivas.SetPixel import set_pixel


# ============================================================
# Função principal
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
    Optimized version using Direct Memory Access (PixelArray) and Texture Matrices.

    Args:
        pixel_array: pygame.PixelArray (locked screen surface)
        screen_w, screen_h: int (screen dimensions)
        vertices_uv: list of (x, y, u, v)
        texture_matrix: list of lists containing colors (pre-loaded texture)
        tex_w, tex_h: int (dimensions of the texture)
        method: 'standard' or 'tiling'
    """
    # Extrai coordenadas Y para definir o range do scanline
    y_values = [v[1] for v in vertices_uv]
    y_min = max(0, int(min(y_values)))
    y_max = min(screen_h, int(max(y_values)))

    # Pré-cálculo de limites para evitar lookups repetidos
    tex_w_max = tex_w - 1
    tex_h_max = tex_h - 1
    n = len(vertices_uv)

    for y in range(y_min, y_max):
        intersecoes = []
        for i in range(n):
            x0, y0, u0, v0 = vertices_uv[i]
            x1, y1, u1, v1 = vertices_uv[(i + 1) % n]

            # Ignora arestas horizontais
            if int(y0) == int(y1):
                continue

            # Garante y0 < y1
            if y0 > y1:
                x0, y0, u0, v0, x1, y1, u1, v1 = x1, y1, u1, v1, x0, y0, u0, v0

            # Verifica scanline
            if y < y0 or y >= y1:
                continue

            # Interpolação Y (calculada uma vez por linha)
            t = (y - y0) / (y1 - y0)
            x = x0 + (x1 - x0) * t
            u = u0 + (u1 - u0) * t
            v = v0 + (v1 - v0) * t

            intersecoes.append((x, u, v))

        # Ordena interseções pelo X
        intersecoes.sort(key=lambda k: k[0])

        # Preenche os pixels entre pares de interseções
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

            # --- OTIMIZAÇÃO 1: Passo Incremental ---
            # Calcula quanto a textura muda por pixel (Slope)
            # Evita divisão dentro do loop
            inv_span = 1.0 / span_width
            u_step = (u_end - u_start) * inv_span
            v_step = (v_end - v_start) * inv_span

            # Clipping Horizontal e Correção de Textura
            x_draw_start = max(0, x_start)
            x_draw_end = min(screen_w, x_end)

            # Se clipamos o início (x negativo), avançamos o UV proporcionalmente
            start_skip = x_draw_start - x_start
            cur_u = u_start + (u_step * start_skip)
            cur_v = v_start + (v_step * start_skip)

            # --- OTIMIZAÇÃO 2: Separação de Loops ---
            # Evita checar "if method == tiling" para cada pixel

            if method == "tiling":
                # Loop Otimizado para TILING (Cabo/Fundo)
                for x in range(x_draw_start, x_draw_end):
                    # Modulo para repetição
                    u_int = int(cur_u) % tex_w
                    v_int = int(cur_v) % tex_h

                    color = texture_matrix[u_int][v_int]
                    if color[3] >= 10:  # Transparência básica
                        pixel_array[x, y] = color

                    cur_u += u_step
                    cur_v += v_step
            else:
                # Loop Otimizado para STANDARD (Objeto Único/Clamp)
                for x in range(x_draw_start, x_draw_end):
                    # Clamp manual (mais rápido que min/max repetidos)
                    u_int = int(cur_u)
                    v_int = int(cur_v)

                    if u_int < 0:
                        u_int = 0
                    elif u_int > tex_w_max:
                        u_int = tex_w_max

                    if v_int < 0:
                        v_int = 0
                    elif v_int > tex_h_max:
                        v_int = tex_h_max

                    color = texture_matrix[u_int][v_int]
                    if color[3] >= 10:
                        pixel_array[x, y] = color

                    cur_u += u_step
                    cur_v += v_step