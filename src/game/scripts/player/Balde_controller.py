"""
Controlador de Movimento do Jogador (Balde).
Gerencia a física (Cinemática) de translação limitando o movimento às bordas lógicas.
"""

from system.transformacoes_geometricas.Transformacoes_Geometricas import transladar_vertices

class BaldeController:

    def __init__(self, vertices, x_min, x_max, game_state, speed=20):
        self.vertices = vertices
        self.x_min = x_min
        self.x_max = x_max
        self.speed = speed
        self.game_state = game_state

    # ======================================================
    # Atualiza navegação
    # ======================================================
    def update(self, input_handler):
        
        # O balde não se move se o jogador estiver congelado pelo Gelo
        if self.game_state.freeze:
            return self.vertices

        # Navegação para direita
        if input_handler.move_right:
            # Calcula o espaço que falta para bater na parede (x_max) baseando-se no vértice do topo-direito
            distancia_parede = self.x_max - self.vertices[1][0]
            if distancia_parede > 0:
                # Anda a velocidade normal, ou anda SÓ o que falta para colar na linha perfeitamente
                passo = min(self.speed, distancia_parede)
                self.vertices = transladar_vertices(self.vertices, passo, 0)

        # Navegação para esquerda
        if input_handler.move_left:
            # Calcula o espaço que falta para bater na parede esquerda (x_min) baseando-se no vértice do topo-esquerdo
            distancia_parede = self.vertices[0][0] - self.x_min
            if distancia_parede > 0:
                passo = min(self.speed, distancia_parede)
                self.vertices = transladar_vertices(self.vertices, -passo, 0)

        return self.vertices