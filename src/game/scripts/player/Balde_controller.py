from src.system.transformacoes_geometricas.Transformacoes_Geometricas import translacao

class BaldeController:

    def __init__(self, vertices, x_min, x_max):

        self.vertices = vertices
        self.x_min = x_min
        self.x_max = x_max


    # ======================================================
    # Atualiza navegação
    # ======================================================

    def update(self, input_handler):

        # Navegação para direita
        if input_handler.move_right:
            if self.vertices[1][0]<=self.x_max:
                self.vertices = translacao(self.vertices, 4, 0)

        # Navegação para esquerda
        if input_handler.move_left:
            if self.vertices[0][0]>=self.x_min:
                self.vertices = translacao(self.vertices, -4, 0)

        return self.vertices


    # ======================================================
    # Retorna índice selecionado
    # ======================================================

    def get_selected_index(self):
        return self.selected


    # ======================================================
    # Retorna opção selecionada
    # ======================================================

    def get_selected_option(self):
        return self.options[self.selected]