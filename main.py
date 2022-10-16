import settings

import pygame
from sys import exit


resolutuion_option = 2



game_screen_res = settings.screen_resolution[resolutuion_option]
SCREEN_WIDTH = game_screen_res[0]
SCREEN_HEIGHT = game_screen_res[1]
car_scale = settings.car_rescale[resolutuion_option]

pygame.init()
ekran = pygame.display.set_mode(game_screen_res)
pygame.display.set_caption('HIGH RIDE')
czas = pygame.time.Clock()

background = pygame.image.load('textures/tlogry.png')
background = pygame.transform.scale(background, game_screen_res)
car_surface = pygame.image.load('textures/auto.png')
car_surface = pygame.transform.rotozoom(car_surface, 180, car_scale)
car_rectangle = car_surface.get_rect(center = (game_screen_res[0] // 2, game_screen_res[1]  - 50))

backgroundsurface = pygame.Surface(game_screen_res)




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    ekran.blit(background,(0,0))
    ekran.blit(car_surface, car_rectangle)

    pygame.display.update()
    czas.tick(60)
