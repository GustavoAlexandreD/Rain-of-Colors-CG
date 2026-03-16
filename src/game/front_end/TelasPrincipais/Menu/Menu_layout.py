class MenuLayout:

    def __init__(self, width, height, options):

        self.width = width
        self.height = height
        self.options = options

        self.buttons = []

        self._build_layout()

    # ------------------------------------------------------

    def _build_layout(self):

        center_x = self.width // 2

        start_y = 420
        spacing = 80

        button_w = 260
        button_h = 50

        self.buttons = []

        for i, option in enumerate(self.options):

            x = center_x - button_w // 2
            y = start_y + i * spacing

            self.buttons.append({
                "rect": (x, y, button_w, button_h),
                "text": option
            })

    # ------------------------------------------------------

    def get_buttons(self):

        return self.buttons