import random

from game.scripts.ObjetosdaChuva.Estrela import Estrela
from game.scripts.ObjetosdaChuva.Gelo import Gelo
from .ObjetosdaChuva.FactoryChuva import FactoryChuva
from .ObjetosdaChuva.Gota import Gota
from .player import Balde


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

        # cores a garantir por ciclo (ordem fixa)
        self._all_colors = [
            (255, 0, 0),    # vermelho
            (0, 0, 255),    # azul
            (0, 255, 0),    # verde
            (255, 255, 0),  # amarelo
            (255, 0, 255)   # roxo
        ]
        self._remaining_colors = list(self._all_colors)

    def update(self, balde, game_state):
        """Atualiza posições, remove objetos fora da tela e gera novos spawns."""
        self._frame += 1

        # 🔥 velocidade global baseada no score (dificuldade progressiva)
        current_speed = game_state.get_current_speed()

        # update objects
        for obj in list(self.objects):

            # ❄️ FREEZE: objetos param completamente
            if not game_state.freeze:

                # 🔥 fator de dificuldade relativo à velocidade base do jogo
                difficulty_factor = current_speed / game_state.base_speed

                # 🔥 aplica velocidade proporcional mantendo identidade do objeto
                # (ex: estrela continua mais lenta que gota)
                obj.speed = obj.base_speed * difficulty_factor

            obj.update()

            # remover quando abaixo do limite inferior
            if obj.is_off_screen(self.height):
                if isinstance(obj, Gota) and obj.color == game_state.current_color and not game_state.star_power:
                    game_state.perder_vida()

                try:
                    self.objects.remove(obj)
                except ValueError:
                    pass

            # checar colisão com o balde
            obj_x, obj_y = obj.get_position()
            x0, y0, x, y = balde.get_dimensions()

            if (x0 <= obj_x <= x) and (y0 <= obj_y <= y) and not game_state.freeze:
                obj.on_collect(game_state)
                self.objects.remove(obj)

                # efeitos visuais no balde
                if game_state.freeze:
                    balde.boundary_color = (30, 40, 60)
                    balde.fill_color = (120, 140, 150)

                elif game_state.star_power:
                    balde.boundary_color = (90, 60, 10)
                    balde.fill_color = (212, 175, 55)

        # spawn periódico (baseado em frames)
        if self._frame % self.spawn_interval == 0:
            self._spawn_one()

    def _spawn_one(self):
        # posição aleatória horizontal
        x = random.uniform(self.x_min, self.x_max)

        # spawn acima da tela (negativo) para cair naturalmente
        y = random.uniform(-self.spawn_above, -10)

        obj = FactoryChuva.create_objeto(x, y)

        # se for Gota, garantir distribuição de cores por ciclo de 10
        if isinstance(obj, Gota):

            # ainda há cores obrigatórias no ciclo
            if self._remaining_colors:
                chosen = self._remaining_colors.pop(0)
                obj.color = chosen
            else:
                # fallback aleatório após garantir todas
                obj.color = random.choice(Gota.COLORS)

            self.gotas_cycle_count += 1

            # reset ciclo a cada 10 gotas
            if self.gotas_cycle_count >= 10:
                self.gotas_cycle_count = 0
                self._remaining_colors = list(self._all_colors)

        self.objects.append(obj)

    def set_area(self, x_min, x_max, spawn_above=None):
        """Configura a área horizontal de spawn e opcionalmente a altura de spawn."""
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