import pygame
import math
import random

from db.storagedriver import StorageDriver
from screen.game_screen_class import GameScreen


class Garage(GameScreen):
    
    

    def __init__(self, w, h):
        super().__init__(w, h)
        
        self.storage_driver = StorageDriver()
        self.coins = self.storage_driver.get_coins()[0]
        # pobera z bazy danych:
        self.is_unlocked = self.set_unlocked()
        self.value = [0,100,2000]
        
        # do testowania!!!!!
        # self.storage_driver.lock_cars()

        self.text1 = self.font.render("select your supercar", True, 'black')
        self.text_rect1 = self.text1.get_rect(center = (self.w//2, 100))
        
        self.coins_txt = self.font.render(f"Coins: {self.coins}", True, 'black')
        self.coins_txt_rect = self.coins_txt.get_rect(center = (self.w//2, 150))
        
        self.menu_button = pygame.image.load('textures/buttons/menubtn.png').convert_alpha()
        self.menu_button_rect = self.menu_button.get_rect(center = (300, 670))
        
        self.select_button = pygame.image.load('textures/buttons/selectbtn.png').convert_alpha()
        self.select_button = pygame.transform.rotozoom(self.select_button, 0, 0.6)
        self.select_button_rect = self.select_button.get_rect(center = (300, self.h//2 - 170))

        self.locked_button = pygame.image.load('textures/buttons/lockedb.png').convert_alpha()
        self.locked_button = pygame.transform.rotozoom(self.locked_button, 0, 0.6)
        self.locked_button_rect = self.locked_button.get_rect(center = (300, self.h//2 + 100))

        self.buy_button = pygame.image.load('textures/buttons/buybtn.png').convert_alpha()
        self.buy_button = pygame.transform.rotozoom(self.buy_button, 0, 0.6)
        self.buy_button_rect = self.buy_button.get_rect(center = (300, self.h//2 + 150))

        self.l_arr = pygame.image.load('textures/buttons/larr.png').convert_alpha()
        self.l_arr_rect = self.l_arr.get_rect(center = (25, self.h//2))
        self.r_arr = pygame.image.load('textures/buttons/rarr.png').convert_alpha()
        self.r_arr_rect = self.r_arr.get_rect(center = (570, self.h//2))

        self.car1 = pygame.image.load('textures/gcars/rcar.png').convert_alpha()
        self.car1_rect = self.car1.get_rect(center = (self.w//2, self.h//2))
        self.car1_text = self.font.render("nissan gtr", True, 'black')
        self.car1_value = self.font.render("", True, 'black')
        self.car1_value_rect = self.car1_value.get_rect(center=(self.w // 2, self.h // 3))

        self.car2 = pygame.image.load('textures/gcars/yelcar.png').convert_alpha()
        self.car2_rect = self.car2.get_rect(center = (self.w//2, self.h//2))
        self.car2_text = self.font.render("Lambo", True, 'black')
        self.car2_value = self.font.render("100 PLN", True, 'black')
        self.car2_value_rect = self.car2_value.get_rect(center=(self.w // 2, self.h // 3))

        self.car3 = pygame.image.load('textures/gcars/supra.png').convert_alpha()
        self.car3_rect = self.car3.get_rect(center = (self.w//2, self.h//2))
        self.car3_text = self.font.render("toyota Supra", True, 'black')
        self.car3_value = self.font.render("2000 PLN", True, 'black')
        self.car3_value_rect = self.car3_value.get_rect(center=(self.w // 2, self.h // 3))


        self.cars = [self.car1, self.car2, self.car3]
        self.cars_txt = [self.car1_text, self.car2_text, self.car3_text]
        self.cars_value =[self.car1_value, self.car2_value, self.car3_value]
        
        self.selected_car = 0
        self.curr_car = self.selected_car

        self.car_text_rect = self.cars_txt[self.curr_car].get_rect(center = (self.w//2, self.h//2 - 100))
        
    def set_unlocked(self):
        '''zwraca ktore auta sa odblokowane z bazy danych'''
        return [self.storage_driver.is_car_unlocked(car_id) for car_id in range(0,3)]
    
    def set_values(self):
        '''zwraca ceny aut z bazy danych'''
        pass
    
    def move_arrow(self):
        # przechodzenie po garażu klikając myszką w przycisk
        # zmień w lewo
        if self.l_arr_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if self.curr_car == 0: 
                self.curr_car = len(self.cars) - 1
            else:    
                self.curr_car -= 1
            self.car_text_rect = self.cars_txt[self.curr_car].get_rect(center = (self.w//2, self.h//2 - 100))
            pygame.time.wait(150)
        
        # zmień w prawo
        if self.r_arr_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if self.curr_car == len(self.cars) - 1:
                self.curr_car = 0
            else:    
                self.curr_car += 1
            self.car_text_rect = self.cars_txt[self.curr_car].get_rect(center = (self.w//2, self.h//2 - 100))
            pygame.time.wait(150)
        
    
    def select_car(self):
        if self.select_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if self.is_unlocked[self.curr_car]:
                self.selected_car = self.curr_car
                self.storage_driver.set_current_car(self.selected_car)
                return True
                # print(self.selected_car)
            return False 

    def unlock_car(self):
        if self.buy_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            pygame.time.wait(150)
            if self.coins >= self.value[self.curr_car]:   #spakowac do jednej funkcji np check if car is affordable
                self.coins -= self.value[self.curr_car]
                self.is_unlocked[self.curr_car] = 1
                # print(self.is_unlocked)
                self.storage_driver.unlock_car(self.curr_car)
                self.storage_driver.set_coins(self.coins)
                self.coins_txt = self.font.render(f"Coins: {self.coins}", True, 'black')
                self.coins_txt_rect = self.coins_txt.get_rect(center=(self.w // 2, 150))
            else:
                pass                

    def get_selected_car(self):
        return self.selected_car       

    def display_select_button(self):
        ''' Funckja która odpowiednio wyświetla przycisk wyboru/blokady i zakupu auta'''
        if self.is_unlocked[self.curr_car]:
            # print(self.is_unlocked)
            self.screen.blit(self.select_button, self.select_button_rect)
        else:
            self.screen.blit(self.locked_button, self.locked_button_rect)
            self.screen.blit(self.buy_button, self.buy_button_rect)
    
    def display_buttons(self):
        self.screen.blit(self.menu_button, self.menu_button_rect)
        self.screen.blit(self.l_arr, self.l_arr_rect)
        self.screen.blit(self.r_arr, self.r_arr_rect)
        self.display_select_button()                    
        
    def display_garage(self):
        self.screen.fill('brown')
        self.screen.blit(self.text1, self.text_rect1)
        self.screen.blit(self.coins_txt, self.coins_txt_rect)

    def display_car(self):
        self.screen.blit(self.cars[self.curr_car], self.car1_rect)
        self.screen.blit(self.cars_txt[self.curr_car], self.car_text_rect)
        self.screen.blit(self.cars_value[self.curr_car], self.car2_value_rect)

    def click_menu_button(self) -> int:
        # !!!! zwraca odpowiedni numer stanu, zgodny z GameState.State
        # 1 - MENU
        
        if self.menu_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return 1
        elif self.select_car():
            return 1
            
        
        