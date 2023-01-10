import pygame
import random
import settings
import math

from character.chr import Character


class Baner(Character):
    
    # baner_pos_list = [(40, 200), (480,200)]
    baner_path_list = ['baner.png', 'banerl.png', 'baneru.png']

    def __init__(self):

        self.x, self.y = 420, -200 # self.get_random_position()
        super().__init__(self.x, self.y)
        
        self.image = pygame.image.load(self.get_obstacle()).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.3)
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.dy = 5 # wartość równa scrollowi mapy - wtedy wygląda jakby się nie ruszało

    
    def get_obstacle(self) -> str:
        return 'textures/' + random.choice(Baner.baner_path_list) 
        
    def get_random_position(self):
        return random.choice(Baner.baner_pos_list)

    def move(self, multiplier = 1):
        self.y += self.dy * multiplier
        
    
        
    
    
