import pygame
import math
import random

import settings



class GameScreen():
    """
    Klasa po któej dziedziczyć będą pozostałe ekrany, tj Mapa, Garaż czy Menu/Options

    w,h - rozdzielczość ekranu
    screen - odpalenie pokazywania ekranu w pygame

    """
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.background = pygame.image.load('textures/tlogry.png').convert_alpha()
        # ile obrazkow ma byc w bufforze
        self.tiles = math.ceil(self.h / self.background.get_height()) + 2
        self.font = pygame.font.Font("textures/font.ttf", 24)
        

    

    def rescale_background(self):
        self.background = pygame.transform.scale(self.background, (self.w, self.h)) 


        







