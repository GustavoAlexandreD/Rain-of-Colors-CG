from system.transformacoes_geometricas.Transformacoes_Geometricas import translacao

class BaldeController:

    def __init__(self, vertices, x_min, x_max, game_state, speed = 10):

        self.vertices = vertices
        self.x_min = x_min
        self.x_max = x_max
        self.speed = speed
        self.game_state = game_state


    # ======================================================
    # Atualiza navegação
    # ======================================================
    def update(self, input_handler):
        # Navegação para direita
        if input_handler.move_right and not self.game_state.freeze:
            # Calcula o espaço que falta para bater na parede (x_max)
            distancia_parede = self.x_max - self.vertices[1][0]
            if distancia_parede > 0:
                # Anda a velocidade normal, ou anda SÓ o que falta para colar na linha
                passo = min(self.speed, distancia_parede)
                self.vertices = translacao(self.vertices, passo, 0)

        # Navegação para esquerda
        if input_handler.move_left and not self.game_state.freeze:
            # Calcula o espaço que falta para bater na parede esquerda (x_min)
            distancia_parede = self.vertices[0][0] - self.x_min
            if distancia_parede > 0:
                passo = min(self.speed, distancia_parede)
                self.vertices = translacao(self.vertices, -passo, 0)

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