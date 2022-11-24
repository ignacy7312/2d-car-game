import pygame
import math
import random

from screen.game_screen_class import GameScreen



class Menu(GameScreen):
    def __init__(self, w, h):
        # pokaz myszke
        pygame.mouse.set_visible(True)
        super().__init__(w, h)
        self.garage_button = pygame.image.load('textures/buttons/garagebtn.png').convert_alpha()
        self.garage_button_rect = self.garage_button.get_rect(center = (300, 470))
        self.start_button = pygame.image.load('textures/buttons/playbtn.png').convert_alpha()
        self.start_button_rect = self.start_button.get_rect(center = (300, 320))
        self.stats_button = pygame.image.load('textures/buttons/statsbtn.png').convert_alpha()
        self.stats_button_rect = self.stats_button.get_rect(center = (300, 620))

        
        # na tym etapie juz useless ale zostawiam bo moze sie przydac
        # self.text1 = self.font.render("press SPACE to start", True, 'black')
        # self.text_rect1 = self.text1.get_rect(center = (self.w//2, self.h//2))
        # self.text2 = self.font.render("press ESC to go to the garage", True, 'black')
        # self.text_rect2 = self.text2.get_rect(center = (self.w//2, self.h//2 - 200))
        self.text1 = self.font.render("press SPACE to start", True, 'black')
        self.text_rect1 = self.text1.get_rect(center = (self.w//2, 140))
        self.text2 = pygame.font.Font("textures/font.ttf", 30).render("WROCLAW MOST WANTED", True, 'black')
        self.text_rect2 = self.text2.get_rect(center = (self.w//2, 80))
        # dodać HIGH SCORE
        self.text3 = self.font.render(f"CURRENT HIGH SCORE: {-1}", True, 'black')
        self.text_rect3 = self.text3.get_rect(center = (self.w//2, 180))


    def display_menu_bg(self):
        self.screen.fill('lightblue')
        self.screen.blit(self.text1, self.text_rect1)
        self.screen.blit(self.text2, self.text_rect2)
        self.screen.blit(self.text3, self.text_rect3)

    def display_buttons(self):
        self.screen.blit(self.garage_button, self.garage_button_rect)
        self.screen.blit(self.start_button, self.start_button_rect)
        self.screen.blit(self.stats_button, self.stats_button_rect)

    def click_button(self) -> int:
        # !!!! zwraca odpowiedni numer stanu, zgodny z GameState.State
        # 2 - GAME, 4 - GARAGE, jeszcze stats nie jest zrobione
        
        if self.garage_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return 4
            # tu powinien zmienić się stan maszyny stanów na garage
        
        if self.start_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return 2
            # tu powinien zmienić się stan maszyny stanów na game (powinna się zacząć gra)
        
        if self.stats_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return None
            # tu powinien zmienić się stan muzyki na off ale nie ma jeszcze muzyki
