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

        #Navegação entre telas
        self.escape = False

        #Zoom da tela de jogo
        self.zoom_in = False
        self.zoom_out = False

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
        self.menu_back = False
        self.pause = False
        self.zoom_in = False
        self.zoom_out = False

        for event in pygame.event.get():

            # ---------------------------------
            # Fechar janela
            # ---------------------------------

            if event.type == pygame.QUIT:
                self.quit = True

            # ---------------------------------
            # TECLADO (pressionou)
            # ---------------------------------

            if event.type == pygame.KEYDOWN:

                # Movimento
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.move_left = True

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.move_right = True

                # Poder especial
                if event.key == pygame.K_SPACE:
                    self.activate_power = True

                # Navegação menu
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.menu_up = True

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.menu_down = True

                if event.key == pygame.K_RETURN:
                    self.menu_select = True

                if event.key == pygame.K_ESCAPE:
                    self.menu_back = True
                
                if event.key == pygame.K_p:
                    self.pause = True

                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.zoom_in = True
                
                if event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
                    self.zoom_out = True

            # ---------------------------------
            # TECLADO (soltou tecla)
            # ---------------------------------

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.move_left = False

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.move_right = False
                
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.zoom_in = False
                
                if event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
                    self.zoom_out = False

            # ---------------------------------
            # MOUSE
            # ---------------------------------

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    self.mouse_click = True
                    self.mouse_pos = pygame.mouse.get_pos()