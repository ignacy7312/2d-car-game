import pygame
import math
import random

from db.storagedriver import StorageDriver
from screen.game_screen_class import GameScreen


class StatsScreen(GameScreen):
    
    

    def __init__(self, w, h):
        super().__init__(w, h)
        
        self.storage_driver = StorageDriver()
        self.high_score = self.storage_driver.get_highscore()[0]
        self.games_played = self.storage_driver.get_games_played()[0]
        self.time_in_game = self.storage_driver.get_total_time_ig()[0]
        self.username = self.storage_driver.get_username()
        # w sumie mozna dodac do db
        self.total_coins_collected = None
        
        self.username_txt = self.font.render(f"Your stats, {self.username}", True, 'black')
        self.username_txt_rect = self.username_txt.get_rect(center = (self.w//2, 100))
        
        self.hs_txt = self.font.render(f"High score: {self.high_score}", True, 'black')
        self.hs_txt_rect = self.hs_txt.get_rect(center = (self.w//2, 150))
        
        self.games_played_txt = self.font.render(f"Total games played: {self.games_played}", True, 'black')
        self.games_played_txt_rect = self.games_played_txt.get_rect(center = (self.w//2, 200))
        
        self.ttig_txt = self.font.render(f"Total time in game: {self.time_in_game} sec", True, 'black')
        self.ttig_txt_rect = self.ttig_txt.get_rect(center = (self.w//2, 250))
        
        self.menu_button = pygame.image.load('textures/buttons/menubtn.png').convert_alpha()
        self.menu_button_rect = self.menu_button.get_rect(center = (300, 720))
        
        
    def display_buttons(self):
        self.screen.blit(self.menu_button, self.menu_button_rect)
        
        
    def display_stats(self):
        self.screen.blit(self.username_txt, self.username_txt_rect)
        self.screen.blit(self.hs_txt, self.hs_txt_rect)
        self.screen.blit(self.games_played_txt, self.games_played_txt_rect)
        self.screen.blit(self.ttig_txt, self.ttig_txt_rect)
        
    def display(self):
        self.screen.fill('grey')
        self.display_stats()
    

    def click_menu_button(self) -> int:
        # !!!! zwraca odpowiedni numer stanu, zgodny z GameState.State
        # 1 - MENU
        
        if self.menu_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return 1
            
            
            
        
        