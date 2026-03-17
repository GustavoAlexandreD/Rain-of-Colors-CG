class JogoLayout:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.center_x = width // 2
        self.center_y = height // 2

    def get_center(self):
        return self.center_x, self.center_y