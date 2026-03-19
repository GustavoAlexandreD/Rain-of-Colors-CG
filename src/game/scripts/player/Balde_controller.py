class BaldeController:

    def __init__(self):

        self.selected = 0


    # ======================================================
    # Atualiza navegação
    # ======================================================

    def update(self, input_handler):

        # Navegação para direita
        if input_handler.move_right:
            self.selected = (self.selected - 1) % len(self.options)

        # Navegação para esquerda
        if input_handler.move_left:
            self.selected = (self.selected + 1) % len(self.options)

        return None


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