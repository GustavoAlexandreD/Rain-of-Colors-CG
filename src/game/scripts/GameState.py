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

        # 🎨 CONTROLE DE TROCA DE COR
        self.catches_for_color_change = 0
        self.catches_to_change_color = 4

        # ❤️ Sistema de vidas
        self.vida = vida

        # 🎨 Cor atual válida
        self.current_color = random.choice(self.COLORS)

        # ⭐ STAR POWER
        self.star_power = False
        self.star_timer = 0

        # ❄️ FREEZE
        self.freeze = False
        self.freeze_timer = 0

        # 🚀 DIFICULDADE (velocidade)
        self.base_speed = 3.0
        self.max_speed = 25.0
        self.speed_increment = 0.1

    # =========================
    # 🎮 UPDATE GLOBAL
    # =========================
    def update(self):
        self._update_star_power()
        self._update_freeze()

    # =========================
    # 🚀 VELOCIDADE PROGRESSIVA
    # =========================
    def get_current_speed(self):
        speed = self.base_speed + (self.score * self.speed_increment / 5)
        return min(speed, self.max_speed)

    # =========================
    # 🎨 TROCA DE COR
    # =========================
    def _change_color(self):
        nova_cor = random.choice(self.COLORS)

        # Evita repetir a mesma cor
        while nova_cor == self.current_color:
            nova_cor = random.choice(self.COLORS)

        self.current_color = nova_cor

    # =========================
    # ⭐ STAR POWER
    # =========================
    def activate_star(self, duration=300):
        if not self.freeze:
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
        if not self.star_power:
            self.freeze = True
            self.freeze_timer = duration

    def _update_freeze(self):
        if self.freeze:
            self.freeze_timer -= 1
            if self.freeze_timer <= 0:
                self.freeze = False

    # =========================
    # 🔥 PONTUAÇÃO + COMBO + TROCA DE COR
    # =========================
    def registrar_acerto(self, pontos_base=10):
        """Registra acerto, aplica combo, pontua e controla troca de cor."""

        # Combo
        self.consecutive_catches += 1
        self.catches_for_color_change += 1

        if self.consecutive_catches % 3 == 0 and self.multiplier < 3:
            self.multiplier += 1

        # Pontuação
        self.score += (pontos_base * self.multiplier)

        # 🔄 Troca de cor a cada N acertos
        if self.catches_for_color_change >= self.catches_to_change_color:
            self._change_color()
            self.catches_for_color_change = 0

    # =========================
    # ❤️ VIDA
    # =========================
    def perder_vida(self):
        self.consecutive_catches = 0
        self.multiplier = 1
        self.catches_for_color_change = 0
        return self.vida.perder_vida()

    # =========================
    # 🔄 RESET
    # =========================
    def reset(self):
        self.score = 0
        self.multiplier = 1
        self.consecutive_catches = 0

        self.catches_for_color_change = 0

        self.current_color = random.choice(self.COLORS)

        self.star_power = False
        self.star_timer = 0

        self.freeze = False
        self.freeze_timer = 0

        self.vida.reset()