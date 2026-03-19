class JogoController:

    def __init__(self):
        self.exit_game = False

    def update(self, input_handler):

        # ESC volta ao menu
        if input_handler.menu_back:
            self.exit_game = True

        return self.exit_game