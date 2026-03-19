import random
from .Gota import Gota
from .Estrela import Estrela
from .Bomba import Bomba
from .Gelo import Gelo


class FactoryChuva:

    @staticmethod
    def create_objeto(x, y):

        rand = random.random()

        if rand < 0.88:
            return Gota(x, y, 40, 20)

        elif rand < 0.86:
            return Estrela(x, y)

        elif rand < 0.93:
            return Gelo(x, y)

        else:
            return Bomba(x, y)