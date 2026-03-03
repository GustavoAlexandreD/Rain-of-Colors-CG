def set_pixel(surface, x, y, color):
    x, y = int(x), int(y)

    width, height = surface.get_size()

    if 0 <= x < width and 0 <= y < height:
        surface.set_at((x, y), color)