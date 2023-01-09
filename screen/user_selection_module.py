import pygame
import math
import random

from db.storagedriver import StorageDriver
from screen.game_screen_class import GameScreen


class UserSelectionScreen(GameScreen):
    
    

    def __init__(self, w, h):
        super().__init__(w, h)
        
        self.storage_driver = StorageDriver()
        self.username_to_choose = ['imie1', 'imie2', 'imie3', 'imie4', 'imie5', 'imie8', 'imie7', 'imie6']
        self.screenpos_y = [200, 300, 400]
        self.user_limit = 4
        
        
        # pobierz z bazy danych id i nazwe aktualnego uzytkownika
        self.curr_id, self.cur_username = self.get_current_user_data()
        # pobierz z bazy danych wszystkie id oraz nazwy uzytkownikow
        self.userids = self.storage_driver.get_all_user_idx()
        assert self.userids, f'puste userids'
        self.usernames = self.storage_driver.get_all_usernames()
        assert self.usernames, f'puste usernames'
        # przypisz id do nazwy
        self.user_id_map = dict((i,j) for i,j in zip(self.userids, self.usernames))
        print(self.user_id_map)
        
        self.user_count = len(self.userids)
        assert self.user_count > 0, f'pusta liczba uzytkownikow'
        
        self.username_txt = self.font.render(f"Current User: {self.cur_username}, id:{self.curr_id}", True, 'black')
        self.username_txt_rect = self.username_txt.get_rect(center = (self.w//2, 140))
        self.limit_txt = self.font.render(f"Limit of users: 3", True, 'black')
        self.limit_txt_rect = self.limit_txt.get_rect(center = (self.w//2, 40))
        self.limit_reached_txt = self.font.render(f"max users created", True, 'black')
        self.limit_reached_txt_rect = self.limit_reached_txt.get_rect(center = (self.w//2, 80))
        
        self.add_user_button = pygame.image.load('textures/buttons/adduserbtn.png').convert_alpha()
        self.add_user_button_rect = self.add_user_button.get_rect(center = (300, 600))
        self.delete_user_button = pygame.image.load('textures/buttons/minideletebtn.png').convert_alpha()
        self.delete_user_button = pygame.transform.rotozoom(self.delete_user_button, 0, 0.7)
        self.select_user_button = pygame.image.load('textures/buttons/miniselectbtn.png').convert_alpha()
        self.select_user_button = pygame.transform.rotozoom(self.select_user_button, 0, 0.7)
        self.menu_button = pygame.image.load('textures/buttons/minimenubtn.png').convert_alpha()
        self.menu_button_rect = self.menu_button.get_rect(center = (500, 720))


        self.text_and_rects_to_display = self.generate_texts_and_rects()
        self.button_rects_to_display = self.generate_button_rects()
        
        
        
        # self.id_to_btn_height_map = dict( (k,m) for k,m in zip(self.userids,[(i[0], i[1]) for i in zip(self.text_and_rects_to_display, self.button_rects_to_display)]))
        
        self.txt_to_bt_rect_map = [(i,j) for i,j in zip(self.text_and_rects_to_display, self.button_rects_to_display)]
        
        # print(self.id_to_btn_height_map[0])
        print(self.user_count, self.userids, self.cur_username, self.usernames)
        # self.create_texts_and_buttons()
        
        
        
    def generate_texts_and_rects(self):
        assert self.user_id_map, f"brak userow i id"
        tmp = []
        j = 0
        for i in zip(self.user_id_map.keys(), self.user_id_map.values()):
            if (i[0] != self.curr_id):
                utxt = self.font.render(f"User:{i[1]}, id:{i[0]}", True, 'black')
                utxt_rect = utxt.get_rect(center = (200, self.screenpos_y[j]))
                tmp.append((utxt, utxt_rect))
                j+=1
        return tmp
    
    def generate_button_rects(self):
        assert self.user_id_map, f"brak userow i id"
        tmp = []
        j = 0
        for i in zip(self.user_id_map.keys(), self.user_id_map.values()):
            if (i[0] != self.curr_id):
                dbt_rect = (i[0], self.delete_user_button.get_rect(center=(450, self.screenpos_y[j])))
                sbt_rect = (i[0], self.select_user_button.get_rect(center=(550, self.screenpos_y[j])))
                #self.id_to_btn_height_map[200 + i*100] = i
                tmp.append((dbt_rect,sbt_rect))
                j+=1
        return tmp
        
        
    def update_mapping(self):
        self.userids = self.storage_driver.get_all_user_idx()
        self.usernames = self.storage_driver.get_all_usernames()
        self.user_count = len(self.userids)
        self.cur_username = self.storage_driver.get_current_username()
        self.curr_id = self.storage_driver.get_current_user_id()
        self.user_id_map = dict((i,j) for i,j in zip(self.userids, self.usernames))
        self.text_and_rects_to_display = self.generate_texts_and_rects()
        self.button_rects_to_display = self.generate_button_rects()    
        self.txt_to_bt_rect_map = [(i,j) for i,j in zip(self.text_and_rects_to_display, self.button_rects_to_display)]
        
        self.username_txt = self.font.render(f"Current User: {self.cur_username}, id:{self.curr_id}", True, 'black')
        self.username_txt_rect = self.username_txt.get_rect(center = (self.w//2, 140))
    
    def get_current_user_data(self):
        ''' Zwraca id i username akrualnego gracza z tabeli polaczenia w bazie danych'''
        return self.storage_driver.get_current_user_id(), self.storage_driver.get_current_username()
    
    def display_buttons(self):
        self.screen.blit(self.menu_button, self.menu_button_rect)
        self.screen.blit(self.add_user_button, self.add_user_button_rect)
        
        
    def display_texts(self):
        self.screen.blit(self.username_txt, self.username_txt_rect)
        self.screen.blit(self.limit_txt, self.limit_txt_rect)
        if self.user_count >= self.user_limit:
            self.screen.blit(self.limit_reached_txt, self.limit_reached_txt_rect)
            
    def display_texts_and_buttons(self):
        for i in self.txt_to_bt_rect_map:
            self.screen.blit(self.delete_user_button, i[1][0][1])
            self.screen.blit(self.select_user_button, i[1][1][1])
            self.screen.blit(i[0][0], i[0][1])
            
            
        
    def display(self):
        self.screen.fill('lightblue')
        self.display_texts()
        self.display_texts_and_buttons()




    def add_user(self):
        if self.user_count < self.user_limit:
            uname = random.choice([i for i in self.username_to_choose if i not in self.usernames])
            self.storage_driver.create_user(uname)
            self.update_mapping()
            


    def delete_user(self):
        # print(self.button_rects_to_display)
        for btn in self.button_rects_to_display:
            if len(self.userids) > 0:
                if btn[0][1].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    print(btn[0])
                    self.storage_driver.delete_user(btn[0][0])
                    self.update_mapping()
                    pygame.time.wait(150)
                
    def select_user(self):
        for btn in self.button_rects_to_display:
                if btn[1][1].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    print("klik klak")
                    self.storage_driver.set_current_user(btn[1][0])
                    self.update_mapping()
                    print(self.cur_username)
                    pygame.time.wait(150)



    def click_menu_button(self) -> int:
        # !!!! zwraca odpowiedni numer stanu, zgodny z GameState.State
        # 1 - MENU
        if self.menu_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return 1


    def click_buttons(self):
        if self.add_user_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.add_user()
            pygame.time.wait(200)
            
            
            
        
        