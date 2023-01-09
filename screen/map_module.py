import pygame
import random


import settings

from screen.game_screen_class import GameScreen
from character.player import Player
from character.obstacle import StaticObstacle, DynamicObstacle
from character.coin import Coin
from screen import music

from db.storagedriver import StorageDriver
from pygame import mixer
class Map(GameScreen):

    """
    Klasa mapy

    
    player1 - gracz
    obs - przeszkoda
    game_speed - prędkość gry
    baner - element mapy, kierunek wyspa słodowa
    """

    def __init__(self, w, h, selected_player):
        super().__init__(w, h)
        self.font = pygame.font.Font("textures/font.ttf", 16)
        self.baner = pygame.image.load('textures/baner.png').convert_alpha()
        self.baner = pygame.transform.rotozoom(self.baner, 0, 0.30) # powinna być na to funkcja
        # i ogólnie elementy mapy pewnie powinny być w jakiejś liście
        self.baner_rect = self.baner.get_rect(center = (self.w - 150, 300))
        self.game_speed = 1 
        self.player1 = Player(350,670, selected_player) # wstępna pozycja
        self.obstacles = []
        self.life= Life(w, h)
        self.sounds=music.Music()
        self.game_over = False
        
        self.storagedriver = StorageDriver()
        self.highscore = self.storagedriver.get_highscore()[0]
        self.score = 0

        # dodawanie serduszek oraz ich skalowanie, myśle że można to gdzies przenieść w dyskretne miejsce żeby oczy nie bolały


        self.scroll = 0

        self.coins = []
        
        self.playersprite = pygame.sprite.GroupSingle(self.player1)



    def display_bg(self):
        # wyświetl tło 
        #self.background = pygame.transform.scale(self.background, (self.w, self.h))

        i = 0
        while (i < self.tiles):
            self.screen.blit(self.background, (0
                             , self.background.get_height() * - i + self.scroll))
            i += 1

        self.scroll += 5 * self.game_speed

        # resetowanie scrolla
        if abs(self.scroll) > self.background.get_height():
            self.scroll = 0
        


    # -------------DEBUG------------------------
    def display_debug_rect(self):
    
        for point in self.player1.mask.outline():
            x = point[0] + self.player1.x
            y = point[1] + self.player1.y - 55
            pygame.draw.circle(self.screen, 'green', (x,y), 2)

        for obstacle in self.obstacles:
            for point in obstacle.mask.outline():
                x = point[0] + obstacle.x - 28
                y = point[1] + obstacle.y
                pygame.draw.circle(self.screen, 'blue', (x,y), 2)





    def display_score_and_money(self):
        self.calculate_score()
        self.score_txt = self.font.render(f'score: {self.score}', True, 'gold')
        self.score_txt_rect = self.score_txt.get_rect(topleft = (5, 10))
        self.money_txt = self.font.render(f'coins: {self.player1.game_money}', True, 'gold')
        self.money_txt_rect = self.money_txt.get_rect(topleft = (5, 30))
        self.highscore_txt = self.font.render(f'HS: {self.highscore}', True, 'black')
        self.highscore_txt_rect = self.highscore_txt.get_rect(topleft = (5, 50))

        self.screen.blit(self.score_txt, self.score_txt_rect)
        self.screen.blit(self.highscore_txt, self.highscore_txt_rect)
        self.screen.blit(self.money_txt, self.money_txt_rect)
        
    def increase_speed(self):
        # przyspiesz grę co 3 sekundy -- wartości można zmienić
        if round(pygame.time.get_ticks(), -3) % 3000 == 0:
            self.game_speed *= 1.0005
            self.player1.dx *= 1.0005
        #print(self.game_speed)


    def update_characters(self):
        # update na ekranie pozycję gracza i przeszkód
        # oraz sprawdza kolizję 
        self.increase_speed()
        self.add_obstacle()
        self.add_coin()
        
        # ta funkcja zwraca true jezeli gracz straci hp i gra ma sie skonczyc 
        self.game_over = self.check_for_obs_collision()
        
        self.collect_coin()
        self.update_player()
        self.update_obstacles()
        self.update_coins()
                
    def update_player(self):
        #self.player1.move_to_initial_pos()
        if self.check_for_border_collision():
            self.player1.move(self.check_for_border_collision())
            self.player1.rect.x = self.player1.x 
            self.toggle_player_inivincible()
            
            
    def check_for_border_collision(self) -> list[bool, bool]:
        # zwraca kolizję z granicą w postaci dwuelementowej listy
        # w któej idx 0 oznacza kolizję z lewą granicą drogi, a idx 1 oznacza kolizję z prawą granicą drogi
        # jeżeli doda się możliwość przeszkalowania ekranu trzeba też będzie wartości const zmienić na jakieś variable
        if 135 > self.player1.x:
            # kolizja z lewej strony
            return [True, False]
        elif self.player1.rect.right > 465: # or self.player1.rect.left > 405
            # kolizja z prawej strony 
            return [False, True]
        # jeżeli brak kolizji
        return [False, False]

    def update_obstacles(self):
        # aktualizuje pozycje przeszkód i wyświetla je na ekranie
        for obstacle in self.obstacles:
            if obstacle:    
                obstacle.move(self.game_speed)
                obstacle.rect.y = obstacle.y
                if obstacle.y > self.h + 100:
                    # gdy przeszkoda wyjdzie poza ekran jest usuwana z listy i obiekt też jest usuwany
                    self.obstacles.remove(obstacle)
                    del obstacle

    def update_coins(self):
        for coin in self.coins:
            if coin:    
                coin.move(self.game_speed)
                coin.rect.y = coin.y
                if coin.y > self.h + 100:
                    # gdy przeszkoda wyjdzie poza ekran jest usuwana z listy i obiekt też jest usuwany
                    self.coins.remove(coin)
                    del coin

    def check_for_obs_coin_spawn_collision(self, to_be_added) -> bool:
        # sprawdza czy moneta lub przeszkoda do dodania
        # po dodaniu kolidowałaby z już istniejącą 
        for obstacle in self.obstacles:
            if to_be_added.rect.y <= obstacle.rect.y + 130 and to_be_added.rect.x == obstacle.rect.x:
                return True
        for coin in self.coins:
            if to_be_added.rect.y <= coin.rect.y - 45 and to_be_added.rect.x == coin.rect.x:
                return True
        return False

    def add_obstacle(self):
        # dodaje przeszkodę we w miarę losowym momencie, nie może być póki co więcej niż 5 na ekranie
        # sprawdza czy w miejscu gdzie ma się pojawić przeszkoda występuje już jakaś inna przeszkoda
        if random.randint(1, 101) % 50 == 0 and len(self.obstacles) < 5:
            if random.randint(1,9) % 8 == 0:
                obs = StaticObstacle()
            else:
                obs = DynamicObstacle()
            if self.check_for_obs_coin_spawn_collision(obs):
                del obs    
            else:
                self.obstacles.append(obs)

    def add_coin(self):
        # dodanie monety
        if random.randint(1, 100) % 97 == 0 and len(self.coins) < 4:
            coin = Coin()
            if self.check_for_obs_coin_spawn_collision(coin):
                del coin    
            else:
                self.coins.append(coin)

    def collect_coin(self):
        # zbiera monetkę jeżeli auto się z nią zderzy
        for coin in self.coins:
            if pygame.Rect.colliderect(coin.rect, self.player1.rect):
                self.player1.game_money += 1
                self.coins.remove(coin)
                self.sounds.sound_play(2,"./sounds/money.wav")
                del coin
    

    """def check_for_obs_collision(self) -> bool:
        # sprawdza czy występuje kolizja gracza z przeszkodą
        for obstacle in self.obstacles:
            if pygame.Rect.colliderect(obstacle.rect, self.player1.rect) and (not self.player1.invincible) and (not self.player1.is_colliding):
                self.player1.blink_invinc_end_time = pygame.time.get_ticks() + 1000
                self.player1.hp -= 1
                self.obstacles.remove(obstacle)
                self.player1.is_colliding = True
                del obstacle
                # zwraca funkcję sprawdzającą hp, która zwraca True jeżeli HP == 0,
                # czyli ta funkcja zwroci True jezeli gracz straci hp - gra ma sie skonczyc
                return self.life.checking_hp(self.player1)
        self.player1.is_colliding = False
        return False"""


    def check_for_obs_collision(self) -> bool:
        # sprawdza czy występuje kolizja gracza z przeszkodą używając maski - pixel perferct collision
        col = False
       
        for obstacle in self.obstacles:
            # wykorzystanie pygame sprite żeby nie kombinować z dziwnymi obliczeniami
            obs = pygame.sprite.GroupSingle(obstacle) 
            
            if pygame.sprite.spritecollide(self.playersprite.sprite, obs, False, pygame.sprite.collide_mask):
                col = True

            if col and (not self.player1.invincible) and (not self.player1.is_colliding):

                self.player1.blink_invinc_end_time = pygame.time.get_ticks() + 1000
                self.player1.hp -= 1
                self.obstacles.remove(obstacle)
                self.player1.is_colliding = True
                del obstacle
                # zwraca funkcję sprawdzającą hp, która zwraca True jeżeli HP == 0,
                # czyli ta funkcja zwroci True jezeli gracz straci hp - gra ma sie skonczyc
                return self.life.checking_hp(self.player1)
            
        self.player1.is_colliding = False
        return False


    def toggle_player_inivincible(self):
        self.player1.invincible = True if pygame.time.get_ticks() <= self.player1.blink_invinc_end_time + 200 else False
            
    def display_map_elements(self):
        # wyświetla elementy mapy, takie jak np. baner
        self.screen.blit(self.baner, self.baner_rect)


    def display_player(self):
        # FUNKCJA KTORA MIGA GRACZEM
        # miganie gracza chwilę po tym jak zderzy się z przeszkodą
        # czas migania/invcs - jedna sekunda
        # print(self.player1.invincible)
        if pygame.time.get_ticks() <= self.player1.blink_invinc_end_time -800:
            self.player1.display_player(self.player1.blink_image, self.screen)
        elif self.player1.blink_invinc_end_time -600 <= pygame.time.get_ticks() <= self.player1.blink_invinc_end_time -400:
            self.player1.display_player(self.player1.blink_image, self.screen)
        elif self.player1.blink_invinc_end_time -200 <= pygame.time.get_ticks() <= self.player1.blink_invinc_end_time:
            self.player1.display_player(self.player1.blink_image, self.screen)     
        else:
            self.player1.display_character(self.screen)
        
        
    def display_characters(self):
        # wyświetla charactery    
        self.display_player()
        #self.player1.display_character(self.screen)
        
        # debug:
        self.display_debug_rect()
        
        for coin in self.coins:
            coin.display_character(self.screen)

        for obstacle in self.obstacles:
            obstacle.display_character(self.screen)
        

    def calculate_score(self):
        # self.score += int((pygame.time.get_ticks() * self.game_speed**10) // 1000)
        self.score += 1


    def is_game_over(self) -> bool:
        return self.game_over

        
class Life():

    def __init__(self,w ,h):
        self.w=w
        self.h=h
        # dodawanie serduszek oraz ich skalowanie, myśle że można to gdzies przenieść w dyskretne miejsce żeby oczy nie bolały
        self.hp1 = pygame.image.load('textures/serce.png').convert_alpha()
        self.hp2 = pygame.image.load('textures/serce.png').convert_alpha()
        self.hp3 = pygame.image.load('textures/serce.png').convert_alpha()
        self.hp1_rect = self.hp1.get_rect(center=(self.w + 5, self.h - 670))
        self.hp2_rect = self.hp2.get_rect(center=(self.w + 45, self.h - 670))
        self.hp3_rect = self.hp3.get_rect(center=(self.w + 85, self.h - 670))
        self.hp1 = pygame.transform.rotozoom(self.hp1, 0, 0.15)
        self.hp2 = pygame.transform.rotozoom(self.hp2, 0, 0.15)
        self.hp3 = pygame.transform.rotozoom(self.hp3, 0, 0.15)
        self.sound=music.Music()

    def checking_hp(self, player1) -> bool:
        if (player1.hp == 2):
            # print('2')
            self.hp1 = pygame.image.load('textures/kosa.png').convert_alpha()
            self.hp1_rect = self.hp1.get_rect(center=(self.w - 80, self.h - 750))
            self.hp1 = pygame.transform.rotozoom(self.hp1, 0, 0.40)
            self.sound.sound_play(0.5,"./sounds/CJ.wav")
            return False
        elif (player1.hp == 1):
            # print('1')
            self.hp2 = pygame.image.load('textures/kosa.png').convert_alpha()
            self.hp2_rect = self.hp2.get_rect(center=(self.w - 40, self.h - 750))
            self.hp2 = pygame.transform.rotozoom(self.hp2, 0, 0.40)
            self.sound.sound_play(0.5,"./sounds/CJ1.wav")
            return False
        elif (player1.hp == 0):
            self.hp3 = pygame.image.load('textures/kosa.png').convert_alpha()
            self.hp3_rect = self.hp3.get_rect(center=(self.w, self.h - 750))
            self.hp3 = pygame.transform.rotozoom(self.hp3, 0, 0.40)
            self.sound.sound_play(0.5,"./sounds/CJ2.wav")
            # print('deat')
            return True

    def show_life(self, screen):
        screen.blit(self.hp1, self.hp1_rect)
        screen.blit(self.hp2, self.hp2_rect)
        screen.blit(self.hp3, self.hp3_rect)

    