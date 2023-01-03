import pygame
import random
import settings
import math

from character.obstacle import Obstacle

class Coin(Obstacle):
    def __init__(self):
        # konstruktor, nie wymaga argumentów, bo x i y są generowane losowo
        super().__init__()
        self.image = pygame.image.load('textures/moneta.png').convert_alpha()
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.mask = self.get_mask()
        self.dy = 5