class Vida:

    def __init__(self, coracoes=None):
        """
        Gerencia o estado de vidas e delega a UI (`coracoes`) para apagar um coração.
        `coracoes` deve ser uma instância de `Coracoes` (opcional).
        """
        self.max_lives = 3
        self.lives = self.max_lives
        self.coracoes = coracoes

    def perder_vida(self):
        if self.lives <= 0:
            return False
        self.lives -= 1
        if self.coracoes:
            try:
                self.coracoes.apagar()
            except Exception:
                pass
        return True

    def reset(self):
        self.lives = self.max_lives
        if self.coracoes:
            try:
                self.coracoes.reset()
            except Exception:
                pass