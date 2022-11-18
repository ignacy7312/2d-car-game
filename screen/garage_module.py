import pygame
import math
import random

from screen.game_screen_class import GameScreen


class Garage(GameScreen):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.text1 = self.font.render("press m to go back to menu", True, 'black')
        self.text_rect1 = self.text1.get_rect(center = (self.w//2, self.h//2))
        
    def display_garage(self):
        self.screen.fill('brown')
        self.screen.blit(self.text1, self.text_rect1)


