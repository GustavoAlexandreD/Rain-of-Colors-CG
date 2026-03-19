import pygame

from game.scripts.Keyboard_Inputs import InputHandler
from game.front_end.TelasPrincipais.Menu.Menu import Menu
from game.front_end.TelasPrincipais.Jogo.Jogo import Jogo
from game.front_end.TelasPrincipais.Estatisticas.Estatisticas import Estatisticas


def main():

    pygame.init()

    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Rain Of Colors")

    clock = pygame.time.Clock()

    input_handler = InputHandler()

    # ==========================
    # Telas
    # ==========================

    pontuations = ["000000", "000000", "000000", "000000", "000000", "000000", "000000", "000000", "000000", "000000"]
    menu = Menu(WIDTH, HEIGHT)
    game = Jogo(WIDTH, HEIGHT)
    statistics = Estatisticas(WIDTH, HEIGHT, pontuations)

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

            elif option == "ESTATISTICA":
                current_screen = "statistics"

            elif option == "SAIR":
                running = False

        elif current_screen == "game":

            if game.update(input_handler):
                current_screen = "menu"

        elif current_screen == "statistics":

            if statistics.update(input_handler):
                current_screen = "menu"

        # =====================================
        # DRAW
        # =====================================

        screen.fill((0, 0, 0))

        if current_screen == "menu":
            menu.draw(screen)

        elif current_screen == "game":
            game.draw(screen)

        elif current_screen == "statistics":
            statistics.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()