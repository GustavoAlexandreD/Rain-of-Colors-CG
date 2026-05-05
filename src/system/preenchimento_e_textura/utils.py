import pygame


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
            return self.surface.get_at((x, y))
        return ColumnView(self, key)

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            x, y = key

            if isinstance(x, slice) or isinstance(y, slice):
                xs = range(*x.indices(self.width)) if isinstance(x, slice) else [x]
                ys = range(*y.indices(self.height)) if isinstance(y, slice) else [y]

                for i in xs:
                    for j in ys:
                        self.surface.set_at((i, j), value)
            else:
                self.surface.set_at((x, y), value)

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
        return self.pxarray.surface.get_at((self.x, y))

    def __setitem__(self, y, value):
        self.pxarray.surface.set_at((self.x, y), value)