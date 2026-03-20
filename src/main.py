import pygame
import os

from game.scripts.Keyboard_Inputs import InputHandler
from game.front_end.TelasPrincipais.Menu.Menu import Menu
from game.front_end.TelasPrincipais.Jogo.Jogo import Jogo
from game.front_end.TelasPrincipais.Estatisticas.Estatisticas import Estatisticas

ARQUIVO_PONTUACOES = "recordes.txt"

def carregar_pontuacoes():
    """Lê o arquivo de recordes. Se não existir, cria uma lista zerada."""
    if os.path.exists(ARQUIVO_PONTUACOES):
        with open(ARQUIVO_PONTUACOES, "r") as f:
            # Lê as linhas e tira os espaços/quebras de linha
            linhas = [linha.strip() for linha in f.readlines() if linha.strip()]
            
            # Garante que sempre teremos 10 posições, mesmo se o arquivo estiver incompleto
            while len(linhas) < 10:
                linhas.append("000000")
            return linhas[:10]
    else:
        # Se for a primeira vez rodando o jogo, retorna 10 zeros
        return ["000000"] * 10

def salvar_pontuacoes(pontuacoes):
    """Escreve a lista atualizada no arquivo txt."""
    with open(ARQUIVO_PONTUACOES, "w") as f:
        for p in pontuacoes:
            f.write(f"{p}\n")

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

    pontuations = carregar_pontuacoes()
    menu = Menu(WIDTH, HEIGHT)
    game = None
    statistics = None

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

        elif current_screen == "statistics" and statistics is not None:
            statistics.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()