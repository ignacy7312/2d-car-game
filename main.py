import settings
import pygame
from game_screen_class import *
from sys import exit
import enum
import state_machine

class Game:
    
    """
    Główna klasa gry
    w,h - rozdzielczość ekranu
    
    """
    pygame.init()
    pygame.display.set_caption('HIGH RIDE')


    def __init__(self, w: int, h: int, fps: int):
        self.w = w
        self.h = h
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.game_agent = state_machine.GameAgent(self.w, self.h)
        

    def run(self):
        # odpala game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.game_agent.execute()
            
            pygame.display.update()
            self.clock.tick(self.fps)



screen_resolution = (600,800)
SCREEN_WIDTH = screen_resolution[0]
SCREEN_HEIGHT = screen_resolution[1]

def game():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, settings.fps)
    game.run()

if __name__ == '__main__':
    game()



# Na poniższe nie patrzeć, zostaje żeby się nie zgubiło w razie czego
"""resolutuion_option = 1
game_screen_res = settings.screen_resolution[resolutuion_option]
SCREEN_WIDTH = game_screen_res[0]
SCREEN_HEIGHT = game_screen_res[1]
car_scale = settings.car_rescale[resolutuion_option]


# pygame.init()
# ekran = pygame.display.set_mode(game_screen_res)
# pygame.display.set_caption('HIGH RIDE')
# czas = pygame.time.Clock()

# background = pygame.image.load('textures/tlogry.png')
# background = pygame.transform.scale(background, game_screen_res)
# car_surface = pygame.image.load('textures/auto.png')
# car_surface = pygame.transform.rotozoom(car_surface, 180, car_scale)
# car_rectangle = car_surface.get_rect(center = (game_screen_res[0] // 2, game_screen_res[1]  - 50))"""


