class JogoLayout:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.center_x = width // 2
        self.center_y = height // 2

    def get_center(self):
        return self.center_x, self.center_y

    def get_top_left(self, margin_x=30, margin_y=30):
        """Retorna a posição do canto superior esquerdo com uma margem.

        margin_x, margin_y: distância em pixels a partir das bordas esquerda/superior.
        """
        return margin_x, margin_y