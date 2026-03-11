class GameState:

    def __init__(self):

        self.score = 0
        self.lives = 3

        self.current_color = (255, 0, 0)

        self.star_power = False
        self.star_timer = 0

    def update(self):

        if self.star_power:
            self.star_timer -= 1

            if self.star_timer <= 0:
                self.star_power = False