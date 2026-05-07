class JogoController:

    def __init__(self):
        self.exit_game = False
        self.pause = False
        
        self.zoom_in = False
        self.zoom_out = False
        
        self.pan_up = False
        self.pan_down = False
        self.pan_left = False
        self.pan_right = False

    def update(self, input_handler):
        if input_handler.pause:
            self.pause = True

        # ESC volta ao menu
        if input_handler.menu_back:
            self.exit_game = True

        self.zoom_in = input_handler.zoom_in
        self.zoom_out = input_handler.zoom_out
        
        self.pan_up = input_handler.pan_up
        self.pan_down = input_handler.pan_down
        self.pan_left = input_handler.pan_left
        self.pan_right = input_handler.pan_right
        
        return self.exit_game