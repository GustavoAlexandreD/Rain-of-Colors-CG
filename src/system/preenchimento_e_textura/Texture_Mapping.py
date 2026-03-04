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

def scanline_texture_polygon(surface, texture, vertices, uvs):
    """
    Preenche polígono com textura usando interpolação linear.

    vertices -> lista [(x,y), ...]
    uvs      -> lista [(u,v), ...] correspondente a cada vértice
    """

    if len(vertices) < 3:
        return

    tex_width, tex_height = texture.get_size()

    ymin = int(min(y for _, y in vertices))
    ymax = int(max(y for _, y in vertices))

    for y in range(ymin, ymax + 1):

        intersections = []

        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]

            u1, v1 = uvs[i]
            u2, v2 = uvs[(i + 1) % len(vertices)]

            if y1 == y2:
                continue

            if (y >= min(y1, y2)) and (y < max(y1, y2)):

                t = (y - y1) / (y2 - y1)

                x = x1 + t * (x2 - x1)
                u = u1 + t * (u2 - u1)
                v = v1 + t * (v2 - v1)

                intersections.append((x, u, v))

        intersections.sort(key=lambda item: item[0])

        for i in range(0, len(intersections), 2):

            if i + 1 >= len(intersections):
                break

            x_start, u_start, v_start = intersections[i]
            x_end,   u_end,   v_end   = intersections[i + 1]

            x_start = int(round(x_start))
            x_end   = int(round(x_end))

            dx = x_end - x_start

            if dx == 0:
                continue

            for x in range(x_start, x_end + 1):

                t = (x - x_start) / dx

                u = u_start + t * (u_end - u_start)
                v = v_start + t * (v_end - v_start)

                # Converte UV (0-1) para coordenada da textura
                tx = int(u * (tex_width  - 1))
                ty = int(v * (tex_height - 1))

                # Clamp segurança
                tx = max(0, min(tx, tex_width  - 1))
                ty = max(0, min(ty, tex_height - 1))

                color = texture.get_at((tx, ty))
                set_pixel(surface, x, y, color)