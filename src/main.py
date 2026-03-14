import pygame


from game.scripts.Keyboard_Inputs import InputHandler
from game.front_end.Menu import Menu


def main() -> None:

    pygame.init()

    # ======================================================
    # Tela na resolução do monitor
    # ======================================================

    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rain Of Colors")

    clock = pygame.time.Clock()

    # ======================================================
    # Sistemas do jogo
    # ======================================================

    input_handler = InputHandler()
    menu = Menu(WIDTH, HEIGHT)

    running = True

    # ======================================================
    # Loop principal
    # ======================================================

    while running:

        clock.tick(60)

        # ----------------------------------------------
        # Atualiza input
        # ----------------------------------------------

        input_handler.update()

        if input_handler.quit:
            running = False

        # ----------------------------------------------
        # Atualiza menu
        # ----------------------------------------------

        option = menu.update(input_handler)

        if option == "SAIR":
            running = False

        if option == "JOGAR":
            print("Iniciar jogo")

        # ----------------------------------------------
        # Render
        # ----------------------------------------------

        screen.fill((0, 0, 0))

        menu.draw(screen)

        pygame.display.flip()

    pygame.quit()


# ==========================================================
# Entry point
# ==========================================================

if __name__ == "__main__":
    main()