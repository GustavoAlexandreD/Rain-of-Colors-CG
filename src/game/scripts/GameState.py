import random


class GameState:

    COLORS = [
        (255, 0, 0),
        (0, 0, 255),
        (0, 255, 0),
        (255, 255, 0),
        (255, 0, 255)
    ]

    def __init__(self, vida):

        # 🎯 Score
        self.score = 0

        # 🔥 MULTIPLICADOR (COMBO)
        self.multiplier = 1
        self.consecutive_catches = 0

        # ❤️ Sistema de vidas (injeção de dependência)
        self.vida = vida

        # 🎨 Cor atual válida
        self.current_color = random.choice(self.COLORS)
        self.current_color_duration = 500

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
        self._update_color()

    # =========================
    # 🎨 Color
    # =========================
    def _update_color(self):
        self.current_color_duration -=1
        if self.current_color_duration < 0:
            self.current_color = random.choice( self.COLORS)
            self.current_color_duration = 500


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
    # 🔥 SISTEMA DE PONTUAÇÃO E COMBO
    # =========================
    def registrar_acerto(self, pontos_base=10):
        """Registra um acerto, aumenta o combo e soma os pontos multiplicados."""
        self.consecutive_catches += 1

        # A cada 3 gotas seguidas, o multiplicador aumenta em 1!
        if self.consecutive_catches % 3 == 0:
            self.multiplier += 1

        # Soma os pontos com o multiplicador atual
        self.score += (pontos_base * self.multiplier)

    # =========================
    # ❤️ VIDA
    # =========================
    def perder_vida(self):
        self.consecutive_catches = 0
        self.multiplier = 1
        return self.vida.perder_vida()

    def reset(self):
        self.score = 0
        self.score = 0
        self.multiplier = 1
        self.current_color = (255, 0, 0)

        self.star_power = False
        self.star_timer = 0

        self.freeze = False
        self.freeze_timer = 0

        self.vida.reset()