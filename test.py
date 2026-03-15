import pygame
import sys
from src.system.primitivas.SetPixel import set_pixel
from src.game.scripts.ObjetosdaChuva.Bomba import Bomba
from src.game.scripts.ObjetosdaChuva.Estrela import Estrela
from src.game.scripts.ObjetosdaChuva.Gota import Gota

pygame.init()
width, height = 500, 400
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Teste de ponto")
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    surface.fill((255,255,255))
    set_pixel(surface, 150, 200, (0,0,0))
    pygame.display.flip()
pygame.quit()
sys.exit()