import random
import math

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

    def __init__(self, width, height, spawn_interval_frames=30, spawn_above=160):
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

        # NOVO: controle de espaçamento entre objetos
        self.min_spawn_distance = 160
        self.max_spawn_attempts = 10

        # cores a garantir por ciclo (usar nomes conforme Gota.COLORS ordem)
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

        # velocidade global baseada no score
        current_speed = game_state.get_current_speed()

        # update objects
        for obj in list(self.objects):

            # aplicar velocidade dinâmica (se não estiver congelado)
            if not game_state.freeze:
                difficulty_factor = current_speed / game_state.base_speed
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

            # detecção de colisão com o balde
            obj_x, obj_y = obj.get_position()
            x0, y0, x, y = balde.get_dimensions()

            if (x0 <= obj_x <= x) and (y0 <= obj_y <= y) and not game_state.freeze:
                obj.on_collect(game_state)
                self.objects.remove(obj)

                if game_state.freeze:
                    balde.boundary_color = (30, 40, 60)
                    balde.fill_color = (120, 140, 150)
                elif game_state.star_power:
                    balde.boundary_color = (90, 60, 10)
                    balde.fill_color = (212, 175, 55)

        difficulty_factor = current_speed / game_state.base_speed
        intervalo_atual = max(4, int(self.spawn_interval / difficulty_factor))

        # spawn periodico (baseado em frames)
        if self._frame % intervalo_atual == 0:
            self._spawn_one(game_state)

    # =========================
    # 🔥 CONTROLE DE ESPAÇAMENTO
    # =========================
    def _is_position_valid(self, x, y):
        """Verifica se a posição está longe o suficiente de outros objetos."""
        for obj in self.objects:
            ox, oy = obj.get_position()
            dist = math.hypot(x - ox, y - oy)

            if dist < self.min_spawn_distance:
                return False

        return True

    def _spawn_one(self, game_state):
        x = None
        y = None

        # tenta encontrar uma posição válida
        for _ in range(self.max_spawn_attempts):

            x = random.uniform(self.x_min, self.x_max)
            y = random.uniform(-self.spawn_above, -10)

            if not self._is_position_valid(x, y):
                continue

            obj = FactoryChuva.create_objeto(x, y, game_state)

            # se for Gota, garantir distribuição de cores por ciclo de 10 gotas
            if isinstance(obj, Gota):

                if self._remaining_colors:
                    chosen = self._remaining_colors.pop(0)
                    obj.color = chosen
                else:
                    obj.color = random.choice(Gota.COLORS)

                self.gotas_cycle_count += 1

                # quando completar 10 gotas, reiniciar ciclo
                if self.gotas_cycle_count >= 10:
                    self.gotas_cycle_count = 0
                    self._remaining_colors = list(self._all_colors)

            self.objects.append(obj)
            return  # spawn bem sucedido

        # se não conseguiu posição válida, não spawna (evita sobreposição)

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