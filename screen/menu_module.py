import pygame
import math
import random

from db.storagedriver import StorageDriver
from screen.game_screen_class import GameScreen



class Menu(GameScreen):
    def __init__(self, w, h):
        # pokaz myszke
        pygame.mouse.set_visible(True)
        super().__init__(w, h)
        
        self.storage_driver = StorageDriver()
        
        self.garage_button = pygame.image.load('textures/buttons/garagebtn.png').convert_alpha()
        self.garage_button_rect = self.garage_button.get_rect(center = (300, 470))
        self.start_button = pygame.image.load('textures/buttons/playbtn.png').convert_alpha()
        self.start_button_rect = self.start_button.get_rect(center = (300, 320))
        self.stats_button = pygame.image.load('textures/buttons/statsbtn.png').convert_alpha()
        self.stats_button_rect = self.stats_button.get_rect(center = (300, 620))
        self.change_user_button = pygame.image.load('textures/buttons/cubtn.png').convert_alpha()
        self.change_user_button_rect = self.change_user_button.get_rect(center = (300, 750))
        
        # mute / unmute management
        self.mute_button = pygame.image.load('textures/buttons/mutebtn.png').convert_alpha()
        self.mute_button = pygame.transform.rotozoom(self.mute_button, 0, 0.25)
        self.unmute_button = pygame.image.load('textures/buttons/unmutebtn.png').convert_alpha()
        self.unmute_button = pygame.transform.rotozoom(self.unmute_button, 0, 0.12)
        self.soundbtn = None 
        self.soundbtn_rect = None
        self.sounds = self.storage_driver.get_sounds()
        self.create_sound_btn_rects()

        self.high_score = self.storage_driver.get_highscore()[0]
        self.username = self.storage_driver.get_current_username()
        
        self.text1 = self.font.render("press SPACE to start", True, 'black')
        self.text_rect1 = self.text1.get_rect(center = (self.w//2, 180))
        self.text2 = pygame.font.Font("textures/font.ttf", 30).render("WROCLAW MOST WANTED", True, 'black')
        self.text_rect2 = self.text2.get_rect(center = (self.w//2, 80))

        self.text3 = self.font.render(f"CURRENT HIGH SCORE: {self.high_score}", True, 'black')
        self.text_rect3 = self.text3.get_rect(center = (self.w//2, 220))

        self.text4 = self.font.render(f"CURRENT USER: {self.username}", True, 'black')
        self.text_rect4 = self.text4.get_rect(center = (self.w//2, 140))


    def create_sound_btn_rects(self):
        if not self.sounds:
            self.soundbtn = self.unmute_button
            self.soundbtn_rect = self.unmute_button.get_rect(center=(50,750))
        else:
            self.soundbtn = self.mute_button
            self.soundbtn_rect = self.mute_button.get_rect(center=(50,750))
            
    def toggle_sounds(self):
        if self.soundbtn_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.sounds = not self.sounds
            self.storage_driver.set_sounds(self.sounds)
            self.create_sound_btn_rects()
            if not self.sounds:
                pygame.mixer.stop()
            else:
                pygame.mixer.unpause()
            print(self.sounds)
            pygame.time.wait(150)
            
        

    def display_menu_bg(self):
        self.screen.fill('lightblue')
        self.screen.blit(self.text1, self.text_rect1)
        self.screen.blit(self.text2, self.text_rect2)
        self.screen.blit(self.text3, self.text_rect3)
        self.screen.blit(self.text4, self.text_rect4)

    def display_buttons(self):
        self.screen.blit(self.garage_button, self.garage_button_rect)
        self.screen.blit(self.start_button, self.start_button_rect)
        self.screen.blit(self.stats_button, self.stats_button_rect)
        self.screen.blit(self.change_user_button, self.change_user_button_rect)
        self.screen.blit(self.soundbtn, self.soundbtn_rect)

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
            return 5
            # tu powinien zmienić się stan muzyki na off ale nie ma jeszcze muzyki

        if self.change_user_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return 6
            # wejście do ekranu zmiany użytkownika
