class GameState:

    def __init__(self, vida):

        # 🎯 Score
        self.score = 0

        # ❤️ Sistema de vidas (injeção de dependência)
        self.vida = vida

        # 🎨 Cor atual válida
        self.current_color = (255, 0, 0)

        # ⭐ STAR POWER
        self.star_power = False
        self.star_timer = 0

        # ❄️ FREEZE (gelo)
        self.freeze = False
        self.freeze_timer = 0

    # =========================
    # 🎮 UPDATE GLOBAL
    # =========================
    def update(self):

        self._update_star_power()
        self._update_freeze()

    # =========================
    # ⭐ STAR POWER
    # =========================
    def activate_star(self, duration=300):
        self.star_power = True
        self.star_timer = duration

    def _update_star_power(self):
        if self.star_power:
            self.star_timer -= 1
            if self.star_timer <= 0:
                self.star_power = False

    # =========================
    # ❄️ FREEZE
    # =========================
    def activate_freeze(self, duration=180):
        self.freeze = True
        self.freeze_timer = duration

    def _update_freeze(self):
        if self.freeze:
            self.freeze_timer -= 1
            if self.freeze_timer <= 0:
                self.freeze = False

    # =========================
    # ❤️ VIDA
    # =========================
    def perder_vida(self):
        return self.vida.perder_vida()

    def reset(self):
        self.score = 0
        self.current_color = (255, 0, 0)

        self.star_power = False
        self.star_timer = 0

        self.freeze = False
        self.freeze_timer = 0

        self.vida.reset()