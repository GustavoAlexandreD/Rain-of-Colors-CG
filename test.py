import pygame
import sys
from system.primitivas.SetPixel import set_pixel
from game.scripts.ObjetosdaChuva.Bomba import Bomba
from game.scripts.ObjetosdaChuva.Estrela import Estrela
from game.scripts.ObjetosdaChuva.Gota import Gota
from game.front_end.Componentes.Button import Button

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
    surface.fill((255,255,255))
    #V Insira a função de teste aqui V
    botao = Button(surface, 200, 150, 100, 50)
    botao.fill((211,211,211))
    botao.draw((0,0,0), 3)
    

    pygame.display.flip()
pygame.quit()
sys.exit()