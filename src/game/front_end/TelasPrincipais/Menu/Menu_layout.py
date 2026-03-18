from game.front_end.helper.responsive import Responsive


class MenuLayout:

    def __init__(self, width, height, options):
        self.width = width
        self.height = height
        self.options = options

        self.resp = Responsive(width, height)

        self.buttons = []
        self._build_layout()

    def _build_layout(self):

        cx = self.width // 2

        # Responsivo
        button_w = self.resp.wp(0.18)
        button_h = self.resp.hp(0.07)

        spacing = self.resp.hp(0.09)
        start_y = self.resp.hp(0.55)

        self.buttons = []

        for i, option in enumerate(self.options):

            x = cx - button_w // 2
            y = start_y + i * spacing

            self.buttons.append({
                "rect": (x, y, button_w, button_h),
                "text": option
            })

    def get_buttons(self):
        return self.buttons