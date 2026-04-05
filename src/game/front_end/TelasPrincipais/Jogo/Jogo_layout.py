from game.front_end.helper.Responsive import Responsive


class JogoLayout:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.resp = Responsive(width, height)

        self.center_x = width // 2
        self.center_y = height // 2

    def get_center(self):
        return self.center_x, self.center_y

    def get_top_left(self, margin_x=0.03, margin_y=0.05):
        return self.resp.wp(margin_x), self.resp.hp(margin_y)

    # -------------------------
    # CHUVA RESPONSIVA
    # -------------------------
    def set_rain_area_with_margins(self):

        self.rain_x_min = self.resp.wp(0.03)
        self.rain_x_max = self.resp.wp(0.66)
        self.spawn_above = int(self.height * 1.5)

    def get_rain_area(self):
        return self.rain_x_min, self.rain_x_max, self.spawn_above