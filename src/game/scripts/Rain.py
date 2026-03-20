import random
from time import perf_counter

from .ObjetosdaChuva.FactoryChuva import FactoryChuva
from .ObjetosdaChuva.Gota import Gota


class Rain:
    """Gerencia o spawn e atualização dos objetos da chuva.

    Regras implementadas:
    - Usa `FactoryChuva.create_objeto(x,y)` para criar objetos.
    - Gotas (Gota) têm garantia de distribuição: a cada 10 gotas spawnadas
      haverá pelo menos 1 de cada cor (vermelho, verde, amarelo, azul, roxo).
    - Spawn ocorre acima da área visível (y negativo) numa faixa configurável.
    - Objetos são removidos quando ultrapassam o limite inferior (`height`).
    """

    def __init__(self, width, height, spawn_interval_frames=48, spawn_above=160):
        self.width = width
        self.height = height

        # lista de objetos ativos
        self.objects = []

        # controle de spawn (em frames)
        self.spawn_interval = max(1, int(spawn_interval_frames))
        self._frame = 0

        # distância acima da tela onde os objetos podem nascer (y negativo)
        self.spawn_above = spawn_above

        # área horizontal de spawn (padrão com margens)
        self.x_min = 20
        self.x_max = max(20, width - 20)

        # controle de distribuição de cores das gotas
        self.gotas_cycle_count = 0
        # cores a garantir por ciclo (usar nomes conforme Gota.COLORS ordem)
        self._all_colors = [
            (255, 0, 0),    # vermelho
            (0, 0, 255),    # azul
            (0, 255, 0),    # verde
            (255, 255, 0),  # amarelo
            (255, 0, 255)   # roxo
        ]
        self._remaining_colors = list(self._all_colors)

    def update(self, game_state):
        """Atualiza posições, remove objetos fora da tela e gera novos spawns."""

        self._frame += 1

        # update objects
        for obj in list(self.objects):
            obj.update()
            # remover quando abaixo do limite inferior
            if obj.is_off_screen(self.height):
                if isinstance(obj, Gota) and obj.color == game_state.current_color or game_state.star_power:
                    game_state.perder_vida()

                try:
                    self.objects.remove(obj)
                except ValueError:
                    pass

        # spawn periodico (baseado em frames)
        if self._frame % self.spawn_interval == 0:
            self._spawn_one()

    def _spawn_one(self):
        x = random.uniform(self.x_min, self.x_max)
        # spawn acima da tela (negativo) para só aparecer depois
        y = random.uniform(-self.spawn_above, -10)

        obj = FactoryChuva.create_objeto(x, y)

        # se for Gota, garantir distribuição de cores por ciclo de 10 gotas
        if isinstance(obj, Gota):
            # se ainda houver cores não garantidas, atribui uma delas
            if self._remaining_colors:
                # escolher uma cor da lista remaining (pop last)
                chosen = self._remaining_colors.pop(0)
                obj.color = chosen
            else:
                # cor aleatória normal
                obj.color = random.choice(Gota.COLORS)

            self.gotas_cycle_count += 1

            # quando completar 10 gotas, reiniciar ciclo
            if self.gotas_cycle_count >= 10:
                self.gotas_cycle_count = 0
                self._remaining_colors = list(self._all_colors)

        self.objects.append(obj)

    def set_area(self, x_min, x_max, spawn_above=None):
        """Configura a área horizontal de spawn e opcionalmente a distância acima da tela."""
        self.x_min = x_min
        self.x_max = x_max
        if spawn_above is not None:
            self.spawn_above = spawn_above

    def draw(self, surface):
        # desenha todos os objetos na ordem atual
        for obj in self.objects:
            try:
                obj.draw(surface)
            except Exception:
                pass

    def clear(self):
        self.objects.clear()
