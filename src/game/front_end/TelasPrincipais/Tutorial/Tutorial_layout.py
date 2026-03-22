from game.front_end.helper.Responsive import Responsive

class TutorialLayout:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.resp = Responsive(width, height)

        self.center_x = width // 2
        self.center_y = height // 2
        self.instructions_positions = self._build_layout()

    def get_center(self):
        return self.center_x, self.center_y
    
    def _build_layout(self):

        # Responsivo
        panel_w = self.resp.wp(0.80)
        panel_h = self.resp.hp(0.90)
        start_y = self.resp.hp(0.06)

        spacing = self.resp.hp(0.082)

        self.panel = (self.center_x, self.center_y, panel_w, panel_h)
        instructions = ["OBJETIVO: O JOGADOR DEVE MOVIMENTAR UM BALDE PARA CAPTURAR AS GOTAS DA COR INDICADA E EVITAR OBSTACULOS.",
                        "O JOGADOR TEM ATE 3 VIDAS(CORACOES) E PERDE UMA VIDA A CADA GOTA DA COR INDICADA PERDIDA OU CAPTURANDO UMA GOTA DE OUTRA COR.",
                        "COMO JOGAR",
                        "->/d: MOVIMENTA O BALDE PARA A DIREITA.",
                        "<-/a: MOVIMENTA O BALDE PARA A ESQUERDA.",
                        "OBSTACULOS",
                        "ESTRELA: PERMITE O JOGADOR GANHAR PONTOS COM GOTAS DE QUALQUER COR.",
                        "GELO: O JOGADOR E CONGELADO E IMPEDIDO DE CAPTURAR OUTROS ITENS.",
                        "BOMBA: O JOGADOR PERDE AUTOMATICAMENTE."]

        ordem = 1
        instructions_positions = []
        for instruction in instructions:

            x = self.center_x
            y = start_y + ordem * spacing
            if y < (start_y + panel_h - spacing):
                instructions_positions.append({
                    "x": x,
                    "y": y,
                    "text": instruction
                })
                ordem += 1
            else:
                break

        return instructions_positions

    def get_panel(self):
        return self.panel, self.instructions_positions
        