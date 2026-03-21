class Responsive:
    BASE_W = 1920
    BASE_H = 1080

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.scale_x = width / self.BASE_W
        self.scale_y = height / self.BASE_H

        # Mantém proporção (importante)
        self.scale = min(self.scale_x, self.scale_y)

    # ----------------------------
    # ESCALA BASEADA EM 1920x1080
    # ----------------------------
    def s(self, value):
        return int(value * self.scale)

    # ----------------------------
    # PORCENTAGEM
    # ----------------------------
    def wp(self, percent):
        return int(self.width * percent)

    def hp(self, percent):
        return int(self.height * percent)

    # ----------------------------
    # FONTE
    # ----------------------------
    def font(self, size):
        return int(size * self.scale)