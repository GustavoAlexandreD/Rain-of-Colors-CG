import random
from .Gota import Gota
from .Estrela import Estrela
from .Bomba import Bomba


class FactoryChuva:

    @staticmethod
    def create_objeto(x, y):

        rand = random.random()

        if rand < 0.7:
            return Gota(x, y)

        elif rand < 0.9:
            return Estrela(x, y)

        else:
            return Bomba(x, y)