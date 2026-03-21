import pygame
import sys
from src.game.scripts.player.Balde import Balde

pygame.init()

    # ======================================================
    # Tela na resolução do monitor
    # ======================================================

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rain Of Colors")

clock = pygame.time.Clock()
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    surface.fill((0,0,0))
    #V Insira a função de teste aqui V
    balde = Balde(100, 100)
    balde.draw(surface)

    pygame.display.flip()
pygame.quit()
sys.exit()