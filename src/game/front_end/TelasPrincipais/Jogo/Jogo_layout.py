class JogoLayout:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.center_x = width // 2
        self.center_y = height // 2

    # --------------------
    # POSIÇÕES GERAIS
    # --------------------
    def get_center(self):
        return self.center_x, self.center_y

    def get_top_left(self, margin_x=30, margin_y=30):
        return margin_x, margin_y

    # --------------------
    # CHUVA
    # --------------------
    def set_rain_area(self, x_min, x_max, spawn_above=160):
        x_min = int(x_min)
        x_max = int(x_max)

        if x_min >= x_max:
            raise ValueError("x_min deve ser menor que x_max")

        self.rain_x_min = x_min
        self.rain_x_max = x_max
        self.rain_spawn_above = int(spawn_above)

    def set_rain_area_with_margins(self, left_margin, right_margin, spawn_above=160):
        self.set_rain_area(
            left_margin,
            self.width - right_margin,
            spawn_above
        )

    def get_rain_area(self, default_margin=20, default_spawn_above=160):
        x_min = getattr(self, 'rain_x_min', default_margin)
        x_max = getattr(self, 'rain_x_max', self.width - default_margin)
        spawn_above = getattr(self, 'rain_spawn_above', default_spawn_above)

        return x_min, x_max, spawn_above