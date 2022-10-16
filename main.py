import pygame
from sys import exit
pygame.init()
ekran = pygame.display.set_mode((1920,1080))
pygame.display.set_caption('HIGH RIDE')
czas = pygame.time.Clock()

background = pygame.image.load('/home/robert/cargame/venv/textures/tlogry.png')
car = pygame.image.load('/home/robert/cargame/venv/textures/auto.png')

backgroundsurface = pygame.Surface((1920,1080))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    ekran.blit(background,(0,0))

    pygame.display.update()
    czas.tick(60)
