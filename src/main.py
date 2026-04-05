import pygame
import os

from game.front_end.TelasPrincipais.Tutorial.Tutorial import Tutorial
from game.scripts.Pontuacao import carregar_pontuacoes,salvar_pontuacoes
from game.scripts.Music_manager import play_soundtrack

from game.scripts.Keyboard_Inputs import InputHandler
from game.front_end.TelasPrincipais.Menu.Menu import Menu
from game.front_end.TelasPrincipais.Jogo.Jogo import Jogo
from game.front_end.TelasPrincipais.Estatisticas.Estatisticas import Estatisticas

def main():

    pygame.init()

    try:
        pygame.mixer.init()
        play_soundtrack(volume=0.4)
    except pygame.error as e:
        print(f"Error initializing audio mixer: {e}")

    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Rain Of Colors")

    clock = pygame.time.Clock()

    input_handler = InputHandler()

    # ==========================
    # Telas
    # ==========================

    pontuations = carregar_pontuacoes()
    menu = Menu(WIDTH, HEIGHT)
    game = None
    statistics = None
    tutorial = None

    # Estado atual
    current_screen = "menu"

    running = True

    while running:

        clock.tick(60)

        input_handler.update()

        if input_handler.quit:
            running = False

        # =====================================
        # UPDATE
        # =====================================

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

        elif current_screen == "game":

            if game.update(input_handler):
                pontuacao_final = game.game_state.score

                pontos_ints = [int(p) for p in pontuations]
                pontos_ints.append(pontuacao_final)

                pontos_ints.sort(reverse=True)
                pontos_ints = pontos_ints[:10]

                pontuations = [f"{p:06d}" for p in pontos_ints]

                salvar_pontuacoes(pontuations)
                
                current_screen = "menu"
                game = None
    
            if game is not None:
                if game.controller.pause:
                    option = game.pause.update(input_handler)

                    if option == "CONTINUAR":
                        game.controller.pause = False
                    elif option == "RECOMECAR":
                        game.game_state.reset = True
                        game.controller.pause = False
                        game = None
                        game = Jogo(WIDTH, HEIGHT, screen)
                    elif option == "VOLTAR P/ MENU":
                        game.controller.exit_game = True
                if game.sistema_vida.lives <= 0:
                    option = game.game_over.update(input_handler)

                    if option == "RECOMECAR":
                        game.game_state.reset = True
                        game.controller.pause = False
                        game = None
                        game = Jogo(WIDTH, HEIGHT, screen)
                    elif option == "VOLTAR P/ MENU":
                        game.controller.exit_game = True

        elif current_screen == "tutorial":

            if tutorial.update(input_handler):
                current_screen = "menu"
                tutorial = None

        elif current_screen == "statistics":

            if statistics.update(input_handler):
                current_screen = "menu"
                statistics = None

        # =====================================
        # DRAW
        # =====================================

        screen.fill((0, 0, 0))

        if current_screen == "menu":
            menu.draw(screen)

        elif current_screen == "game" and game is not None:
            game.draw(screen)

        elif current_screen == "tutorial" and tutorial is not None:
            tutorial.draw(screen)

        elif current_screen == "statistics" and statistics is not None:
            statistics.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()