import pygame
import math
import random

from screen.game_screen_class import GameScreen



class Menu(GameScreen):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.garage_button = pygame.image.load('textures/buttons/bgr.png').convert_alpha()
        self.garage_button_rect = self.garage_button.get_rect(center = (300, 650))
        self.start_button = pygame.image.load('textures/buttons/butsound.png').convert_alpha()
        self.start_button_rect = self.start_button.get_rect(center = (300, 300))
        self.sound_button = pygame.image.load('textures/buttons/butstart.png').convert_alpha()
        self.sound_button_rect = self.sound_button.get_rect(center = (300, 550))

        
        self.text1 = self.font.render("press SPACE to start", True, 'black')
        self.text_rect1 = self.text1.get_rect(center = (self.w//2, self.h//2))
        self.text2 = self.font.render("press ESC to go to the garage", True, 'black')
        self.text_rect2 = self.text2.get_rect(center = (self.w//2, self.h//2 - 200))

        

    def display_menu_bg(self):
        self.screen.fill('lightblue')
        self.screen.blit(self.text1, self.text_rect1)
        self.screen.blit(self.text2, self.text_rect2)

    def display_buttons(self):
        self.screen.blit(self.garage_button, self.garage_button_rect)
        self.screen.blit(self.start_button, self.start_button_rect)
        self.screen.blit(self.sound_button, self.sound_button_rect)

    def click_button(self):
        if self.garage_button_rect.collidepoint(pygame.mouse.get_pos()):
            pass
        # tu powinien zmienić się stan maszyny stanów na garage
        if self.start_button_rect.collidepoint(pygame.mouse.get_pos()):
            pass
        # tu powinien zmienić się stan maszyny stanów na game (powinna się zacząć gra)
        if self.sound_button_rect.collidepoint(pygame.mouse.get_pos()):
            pass # tu powinien zmienić się stan muzyki na off ale nie ma jeszcze muzyki
