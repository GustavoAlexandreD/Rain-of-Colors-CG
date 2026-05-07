import pygame
from system.primitivas.GetPixel import get_pixel
from system.primitivas.SetPixel import set_pixel

class PixelArrayClone:
    def __init__(self, surface):
        if not isinstance(surface, pygame.Surface):
            raise TypeError("Expected a pygame.Surface")

        self.surface = surface
        self.width, self.height = surface.get_size()
        self.locked = True
        self.surface.lock()

    @property
    def shape(self):
        return (self.width, self.height)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            x, y = key
            return get_pixel(self.surface, x, y)
        return ColumnView(self, key)

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            x, y = key

            if isinstance(x, slice) or isinstance(y, slice):
                xs = range(*x.indices(self.width)) if isinstance(x, slice) else [x]
                ys = range(*y.indices(self.height)) if isinstance(y, slice) else [y]

                for i in xs:
                    for j in ys:
                        set_pixel(self.surface, i, j, value)
            else:
                set_pixel(self.surface, x, y, value)

    def close(self):
        if self.locked:
            self.surface.unlock()
            self.locked = False

    def __del__(self):
        self.close()


class ColumnView:
    def __init__(self, pxarray, x):
        self.pxarray = pxarray
        self.x = x

    def __getitem__(self, y):
        return get_pixel(self.pxarray.surface, self.x, y)

    def __setitem__(self, y, value):
        set_pixel(self.pxarray.surface, self.x, y, value)