class JogoController:

    def __init__(self):
        self.exit_game = False
        self.pause = False
        self.zoom_in = False
        self.zoom_out = False

    def update(self, input_handler):
        if input_handler.pause:
            self.pause = True

        # ESC volta ao menu
        if input_handler.menu_back:
            self.exit_game = True

        self.zoom_in = input_handler.zoom_in
        self.zoom_out = input_handler.zoom_out
        return self.exit_game