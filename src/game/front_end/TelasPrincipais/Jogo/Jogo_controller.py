class JogoController:

    def __init__(self):
        self.exit_game = False
        self.pause = False

    def update(self, input_handler):
        if input_handler.pause:
            self.pause = True

        # ESC volta ao menu
        if input_handler.menu_back:
            self.exit_game = True

        return self.exit_game