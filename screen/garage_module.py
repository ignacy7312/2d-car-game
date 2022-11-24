import pygame
import math
import random

from screen.game_screen_class import GameScreen


class Garage(GameScreen):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.text1 = self.font.render("press m to go back to menu", True, 'black')
        self.text_rect1 = self.text1.get_rect(center = (self.w//2, self.h//2))
        
        self.menu_button = pygame.image.load('textures/buttons/menubtn.png').convert_alpha()
        self.menu_button_rect = self.menu_button.get_rect(center = (300, 670))
        
    def display_buttons(self):
        self.screen.blit(self.menu_button, self.menu_button_rect)
                    
        
    def display_garage(self):
        self.screen.fill('brown')
        self.screen.blit(self.text1, self.text_rect1)

    def click_button(self) -> int:
        # !!!! zwraca odpowiedni numer stanu, zgodny z GameState.State
        # 1 - MENU
        
        if self.menu_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return 1
            # tu powinien zmienić się stan maszyny stanów na garage
        
        