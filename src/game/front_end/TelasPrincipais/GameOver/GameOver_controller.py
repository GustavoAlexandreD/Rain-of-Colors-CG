from src.game.scripts.Music_manager import play_audio


class GameOverController:

    def __init__(self, options):

        self.options = options
        self.selected = 0


    # ======================================================
    # Atualiza navegação
    # ======================================================

    def update(self, input_handler):

        # Navegação para cima
        if input_handler.menu_up:
            self.selected = (self.selected - 1) % len(self.options)
            play_audio("AudioTrocaBotaoRainOfColors")

        # Navegação para baixo
        if input_handler.menu_down:
            self.selected = (self.selected + 1) % len(self.options)
            play_audio("AudioTrocaBotaoRainOfColors")

        # Selecionar opção
        if input_handler.menu_select:
            play_audio("AudioBotaoRainOfColors")
            return self.options[self.selected]

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