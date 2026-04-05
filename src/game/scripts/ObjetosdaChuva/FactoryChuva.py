import random
from .Gota import Gota
from .Estrela import Estrela
from .Bomba import Bomba
from .Gelo import Gelo
from .Coracao import Coracao

class FactoryChuva:

    @staticmethod
    def create_objeto(x, y, game_state):
        rand = random.random()

        # Dificuldade dinâmica baseada no score
        if game_state:
            # A cada 50 pontos, a chance de vir Gota normal cai 1% (até ao limite mínimo de 55%)
            reducao = (game_state.score // 10) * 0.01
            chance_gota = max(0.15, 0.85 - reducao)
        else:
            chance_gota = 0.85

        # O espaço de probabilidade que sobrou (ex: 15% até 45%) é dividido entre os especiais
        sobra = 1.0 - chance_gota

        # Distribuição proporcional da "sobra":
        chance_estrela = chance_gota + (sobra * 0.02) # 20% da sobra para Estrela
        chance_gelo = chance_estrela + (sobra * 0.10) # 30% da sobra para Gelo
        chance_coracao = chance_gelo + (sobra * 0.05) # 10% da sobra para Coração
        # O resto da sobra (40%) fica automaticamente para a Bomba!

        if rand < chance_gota:
            return Gota(x, y, 35, 25)
        elif rand < chance_estrela:
            return Estrela(x, y)
        elif rand < chance_gelo:
            return Gelo(x, y)
        elif rand < chance_coracao:
            return Coracao(x, y)
        else:
            return Bomba(x, y)