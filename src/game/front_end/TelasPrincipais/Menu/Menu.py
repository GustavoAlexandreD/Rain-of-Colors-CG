from src.game.front_end.TelasPrincipais.Menu.Menu_layout import MenuLayout
from src.game.front_end.TelasPrincipais.Menu.Menu_controller import MenuController


class Menu:

    def __init__(self, width, height):

        self.options = [
            "JOGAR",
            "ESTATISTICA",
            "SAIR"
        ]

        self.layout = MenuLayout(width, height, self.options)
        self.controller = MenuController(self.options)

        self.buttons = self.layout.get_buttons()


    # --------------------------------
    # Update
    # --------------------------------

    def update(self, input_handler):

        return self.controller.update(input_handler)


    # --------------------------------
    # Retorna botão selecionado
    # --------------------------------

    def get_selected(self):

        return self.controller.get_selected_index()