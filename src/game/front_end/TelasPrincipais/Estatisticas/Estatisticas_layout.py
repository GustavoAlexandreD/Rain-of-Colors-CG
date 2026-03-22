from game.front_end.Componentes.TelaSuspensa import TelaSuspensa
from game.front_end.helper.Responsive import Responsive

class StatisticsLayout:

    def __init__(self, width, height, pontuations):
        self.width = width
        self.height = height
        self.pontuations = pontuations

        self.resp = Responsive(width, height)

        self.center_x = width // 2
        self.center_y = height // 2
        self._build_layout()

    def get_center(self):
        return self.center_x, self.center_y
    
    def _build_layout(self):

        # Responsivo
        panel_w = self.resp.wp(0.80)
        panel_h = self.resp.hp(0.90)
        start_y = self.resp.hp(0.06)

        spacing = self.resp.hp(0.082)

        self.panel = (self.center_x, self.center_y, panel_w, panel_h)
        self.pontuations_positions = []

        ordem = 1
        for pontuation in self.pontuations:

            text = f"{ordem} - {pontuation}"

            x = self.center_x
            y = start_y + ordem * spacing
            if y<(start_y + panel_h - spacing):
                self.pontuations_positions.append({
                    "x": x,
                    "y": y,
                    "text": text
                })
                ordem +=1
            else:
                break

    def get_panel(self):
        return self.panel, self.pontuations_positions
        