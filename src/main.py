"""
Ponto de entrada principal do jogo Rain of Colors.

Este módulo é responsável por inicializar o motor gráfico (Pygame),
configurar o display em tela cheia, gerenciar o sistema de áudio e
executar o Loop Principal (Game Loop). Ele atua como uma Máquina de
Estados (State Machine), controlando a transição entre o Menu, o
Jogo, o Tutorial e a tela de Estatísticas.
"""

import pygame
import os

from game.front_end.TelasPrincipais.Tutorial.Tutorial import Tutorial
from game.scripts.Pontuacao import carregar_pontuacoes, salvar_pontuacoes
from game.scripts.Music_manager import play_soundtrack
from game.scripts.Keyboard_Inputs import InputHandler
from game.front_end.TelasPrincipais.Menu.Menu import Menu
from game.front_end.TelasPrincipais.Jogo.Jogo import Jogo
from game.front_end.TelasPrincipais.Estatisticas.Estatisticas import Estatisticas

def atualizar_recordes(nova_pontuacao, lista_pontuacoes_str):
    """
    Atualiza a lista de recordes mantendo apenas os 10 maiores placares.
    Converte as strings para inteiros, ordena e devolve formatado com 6 dígitos.
    """
    pontos_ints = [int(p) for p in lista_pontuacoes_str]
    pontos_ints.append(nova_pontuacao)
    
    # Ordena do maior para o menor e mantém os Top 10
    pontos_ints.sort(reverse=True)
    pontos_ints = pontos_ints[:10]
    
    # Retorna formatado com zeros à esquerda (ex: "001500")
    return [f"{p:06d}" for p in pontos_ints]


def main():
    """
    Função principal que inicia e mantém o ciclo de vida do jogo.
    """
    pygame.init()

    # Inicialização do sistema de áudio
    try:
        pygame.mixer.init()
        play_soundtrack(volume=0.4)
    except pygame.error as e:
        print(f"Erro ao inicializar o mixer de áudio: {e}")

    # Configuração de Tela Cheia
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Rain Of Colors")

    clock = pygame.time.Clock()
    input_handler = InputHandler()

    # ==========================
    # Instanciamento de Telas
    # ==========================
    pontuations = carregar_pontuacoes()
    menu = Menu(WIDTH, HEIGHT)
    game = None
    statistics = None
    tutorial = None

    current_screen = "menu"
    running = True

    # ==========================
    # GAME LOOP
    # ==========================
    while running:

        clock.tick(60) # Limita a taxa de atualização a 60 FPS
        input_handler.update()

        if input_handler.quit:
            running = False

        # -----------------------------------
        # 1. ATUALIZAÇÃO LÓGICA (UPDATE)
        # -----------------------------------
        if current_screen == "menu":
            option = menu.update(input_handler)

            if option == "JOGAR":
                current_screen = "game"
                game = Jogo(WIDTH, HEIGHT, screen)
            elif option == "TUTORIAL":
                current_screen = "tutorial"
                tutorial = Tutorial(WIDTH, HEIGHT, pontuations)
            elif option == "ESTATISTICA":
                current_screen = "statistics"
                statistics = Estatisticas(WIDTH, HEIGHT, pontuations)
            elif option == "SAIR":
                running = False

        elif current_screen == "game" and game is not None:
            
            # Atualiza o jogo principal
            if game.update(input_handler):
                # O jogo emitiu um sinal de saída (Fim de jogo tradicional)
                pontuations = atualizar_recordes(game.game_state.score, pontuations)
                salvar_pontuacoes(pontuations)
                current_screen = "menu"
                game = None
    
            # Verifica as telas de sobreposição (Pause e Game Over)
            if game is not None:
                if game.controller.pause:
                    option = game.pause.update(input_handler)

                    if option == "CONTINUAR":
                        game.controller.pause = False
                    elif option == "RECOMECAR":
                        game = Jogo(WIDTH, HEIGHT, screen) # Recria a instância limpa
                    elif option == "VOLTAR P/ MENU":
                        current_screen = "menu"
                        game = None
                        
                elif game.sistema_vida.lives <= 0:
                    option = game.game_over.update(input_handler)

                    if option == "RECOMECAR":
                        game = Jogo(WIDTH, HEIGHT, screen)
                    elif option == "VOLTAR P/ MENU":
                        pontuations = atualizar_recordes(game.game_state.score, pontuations)
                        salvar_pontuacoes(pontuations)
                        current_screen = "menu"
                        game = None

        elif current_screen == "tutorial" and tutorial is not None:
            if tutorial.update(input_handler):
                current_screen = "menu"
                tutorial = None

        elif current_screen == "statistics" and statistics is not None:
            if statistics.update(input_handler):
                current_screen = "menu"
                statistics = None

        # -----------------------------------
        # 2. RENDERIZAÇÃO GRÁFICA (DRAW)
        # -----------------------------------
        screen.fill((0, 0, 0)) # Limpa o buffer de vídeo anterior

        if current_screen == "menu":
            menu.draw(screen)
        elif current_screen == "game" and game is not None:
            game.draw(screen)
        elif current_screen == "tutorial" and tutorial is not None:
            tutorial.draw(screen)
        elif current_screen == "statistics" and statistics is not None:
            statistics.draw(screen)

        pygame.display.flip() # Troca os buffers e exibe na tela

    pygame.quit()

if __name__ == "__main__":
    main()