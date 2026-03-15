def set_pixel(surface, x, y, color):
    x, y = int(x), int(y)

    width = surface.get_width()
    height = surface.get_height()

    if 0 <= x < width and 0 <= y < height:
        surface.set_at((x, y), color)