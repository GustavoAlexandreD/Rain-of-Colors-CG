from src.game.front_end.helper.Responsive import Responsive

class GameOverLayout:

    def __init__(self, width, height, options):
        self.width = width
        self.height = height
        self.options = options

        self.resp = Responsive(width, height)

        self.center_x = width // 2
        self.center_y = height // 2

        self.buttons = []
        self._build_layout()

    def get_center(self):
        return self.center_x, self.center_y
    
    def _build_layout(self):
        cx = self.width // 2
        cy = self.height // 2

        # Responsivo
        panel_w = self.resp.wp(0.35)
        panel_h = self.resp.hp(0.50)

        self.panel = (cx, cy, panel_w, panel_h)

        # Responsivo
        button_w = self.resp.wp(0.18)
        button_h = self.resp.hp(0.07)

        spacing = self.resp.hp(0.09)
        start_y = self.resp.hp(0.45)

        self.buttons = []

        for i, option in enumerate(self.options):

            x = cx - button_w // 2
            y = start_y + i * spacing

            self.buttons.append({
                "rect": (x, y, button_w, button_h),
                "text": option
            })

    def get_panel(self):
        return self.panel
    
    def get_buttons(self):
        return self.buttons
        