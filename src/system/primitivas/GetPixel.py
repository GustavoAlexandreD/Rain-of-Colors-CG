def get_pixel(surface, x, y):
    x, y = int(x), int(y)

    width = surface.get_width()
    height = surface.get_height()

    if 0 <= x < width and 0 <= y < height:
        return surface.get_at((x, y))