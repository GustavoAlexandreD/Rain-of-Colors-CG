import random
from .Gota import Gota
from .Estrela import Estrela
from .Bomba import Bomba
from .Gelo import Gelo
from .Coracao import Coracao


class FactoryChuva:

    @staticmethod
    def create_objeto(x, y):

        rand = random.random()

        if rand < 0.85:
            return Gota(x, y, 35, 25)

        elif rand < 0.88:
            return Estrela(x, y)

        elif rand < 0.93:
            return Gelo(x, y)

        elif rand < 0.95:
            return Coracao(x, y)  # 👈 NOVO

        else:
            return Bomba(x, y)