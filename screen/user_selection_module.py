import pygame
import math
import random

from db.storagedriver import StorageDriver
from screen.game_screen_class import GameScreen


class UserSelectionScreen(GameScreen):
    
    

    def __init__(self, w, h):
        super().__init__(w, h)
        
        self.storage_driver = StorageDriver()
        self.username = self.storage_driver.get_current_username()
        self.username_to_choose = ['imie1', 'imie2', 'imie3', 'imie4', 'imie5']

        self.user_limit = 4
        self.userids = self.storage_driver.get_all_user_idx()
        self.usernames = self.storage_driver.get_all_usernames()
        
        self.user_count = len(self.userids)
        
        self.username_txt = self.font.render(f"Current User: {self.username}", True, 'black')
        self.username_txt_rect = self.username_txt.get_rect(center = (self.w//2, 140))

        self.limit_txt = self.font.render(f"Limit of users: 3", True, 'black')
        self.limit_txt_rect = self.limit_txt.get_rect(center = (self.w//2, 40))

        self.limit_reached_txt = self.font.render(f"max users created", True, 'black')
        self.limit_reached_txt_rect = self.limit_reached_txt.get_rect(center = (self.w//2, 80))
        
        self.add_user_button = pygame.image.load('textures/buttons/adduserbtn.png').convert_alpha()
        self.add_user_button_rect = self.add_user_button.get_rect(center = (300, 600))

        self.delete_user_button = pygame.image.load('textures/buttons/deluserbtn.png').convert_alpha()
        self.delete_user_button = pygame.transform.rotozoom(self.delete_user_button, 0, 0.7)

        
        self.menu_button = pygame.image.load('textures/buttons/minimenubtn.png').convert_alpha()
        self.menu_button_rect = self.menu_button.get_rect(center = (500, 720))


        self.texts_to_display = []
        self.buttons_to_display = []
        self.usernames_wo_current = [uname for uname in self.usernames if uname != self.username]
        self.id_to_btn_height_map = {}

        self.create_texts_and_buttons()
        
        
    def display_buttons(self):
        self.screen.blit(self.menu_button, self.menu_button_rect)
        self.screen.blit(self.add_user_button, self.add_user_button_rect)
        
        
    def display_texts(self):
        self.screen.blit(self.username_txt, self.username_txt_rect)
        self.screen.blit(self.limit_txt, self.limit_txt_rect)
        if self.user_count >= self.user_limit:
            self.screen.blit(self.limit_reached_txt, self.limit_reached_txt_rect)
            
        
    def display(self):
        self.screen.fill('lightblue')
        self.display_texts()
        self.display_users()
        #print(self.id_to_btn_height_map)
        self.get_id_to_delete()

    

    def display_users(self):
        for i in zip(self.buttons_to_display, self.texts_to_display):
            self.screen.blit(self.delete_user_button, i[0])
            self.screen.blit(i[1][0], i[1][1])

    def create_texts_and_buttons(self):
        for i, udata in enumerate(zip(self.userids, self.usernames_wo_current)):
            utxt = self.font.render(f"User:{udata[1]}, id:{udata[0]}", True, 'black')
            utxt_rect = utxt.get_rect(center = (200, 200 + i*100))
            bt_rect = self.delete_user_button.get_rect(center=(500, 200+ i*100))
            self.id_to_btn_height_map[200 + i*100] = udata[0]
            self.texts_to_display.append((utxt, utxt_rect))
            self.buttons_to_display.append(bt_rect)

    def add_user(self):
        if self.user_count < self.user_limit:
            uname = random.choice([i for i in self.username_to_choose if i not in self.usernames])
            self.storage_driver.create_user(uname)
            self.userids = self.storage_driver.get_all_user_idx()
            self.usernames = self.storage_driver.get_all_usernames()
            self.usernames_wo_current = self.usernames.remove(self.username)
            self.create_texts_and_buttons()


    def delete_user(self):
        for btn in self.buttons_to_display:
            if btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.storage_driver.delete_user(self.id_to_btn_height_map[btn.center[1]])
                self.userids = self.storage_driver.get_all_user_idx()
                self.usernames = self.storage_driver.get_all_usernames()
                self.usernames_wo_current = self.usernames.remove(self.username)
                self.create_texts_and_buttons()
                pygame.time.wait(150)

    def get_id_to_delete(self):
        for btn in self.buttons_to_display:
            if btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                pygame.time.wait(150)
                print(self.id_to_btn_height_map[btn.center[1]])
                return self.id_to_btn_height_map[btn.center[1]]

    def select_user(self):
        pass

    def click_menu_button(self) -> int:
        # !!!! zwraca odpowiedni numer stanu, zgodny z GameState.State
        # 1 - MENU
        if self.menu_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return 1


    def click_buttons(self):
        if self.add_user_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.add_user()
            pygame.time.wait(200)
            
            
            
        
        