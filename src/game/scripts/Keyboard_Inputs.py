import pygame


# ==========================================================
# Classe de Controle de Input
# ==========================================================

class InputHandler:
    def __init__(self):
        # Movimento
        self.move_left = False
        self.move_right = False

        # Ação especial
        self.activate_power = False

        # Navegação de menu
        self.menu_up = False
        self.menu_down = False
        self.menu_select = False

        # Mouse
        self.mouse_click = False
        self.mouse_pos = (0, 0)

        # Controle interno
        self.quit = False


    # ======================================================
    # Atualiza estados a cada frame
    # ======================================================

    def update(self):
        # Reset de ações momentâneas
        self.activate_power = False
        self.menu_up = False
        self.menu_down = False
        self.menu_select = False
        self.mouse_click = False

        for event in pygame.event.get():

            # Fechar janela
            if event.type == pygame.QUIT:
                self.quit = True

            # -------------------------
            # TECLADO (pressionado)
            # -------------------------
            if event.type == pygame.KEYDOWN:

                # Movimento
                if event.key == pygame.K_LEFT:
                    self.move_left = True

                if event.key == pygame.K_RIGHT:
                    self.move_right = True

                # Poder especial
                if event.key == pygame.K_SPACE:
                    self.activate_power = True

                # Menu navegação
                if event.key == pygame.K_UP:
                    self.menu_up = True

                if event.key == pygame.K_DOWN:
                    self.menu_down = True

                if event.key == pygame.K_RETURN:
                    self.menu_select = True

            # -------------------------
            # TECLADO (soltou tecla)
            # -------------------------
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT:
                    self.move_left = False

                if event.key == pygame.K_RIGHT:
                    self.move_right = False

            # -------------------------
            # MOUSE
            # -------------------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # botão esquerdo
                    self.mouse_click = True
                    self.mouse_pos = pygame.mouse.get_pos()