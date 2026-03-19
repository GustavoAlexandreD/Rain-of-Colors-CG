class StatisticsController:

    def __init__(self):
        self.exit_stats = False

    def update(self, input_handler):

        if input_handler.menu_back:
            self.exit_stats = True

        return self.exit_stats