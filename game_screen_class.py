import settings
from character import *
import math

import pygame

class GameScreen():


    """
    Klasa po któej dziedziczyć będą pozostałe ekrany, tj Mapa, Garaż czy Menu/Options

    w,h - rozdzielczość ekranu
    screen - odpalenie pokazywania ekranu w pygame

    self.font = pygame.font.Font("textures/font.ttf", 24)
    """
    
    
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.scroll = 0
        self.background = pygame.image.load('textures/tlogry.png').convert_alpha()
        # ile obrazkow ma byc w bufforze
        self.tiles = math.ceil(self.h / self.background.get_height()) + 2
        self.font = pygame.font.Font("textures/font.ttf", 24)
        

    

    def rescale_background(self):
        self.background = pygame.transform.scale(self.background, (self.w, self.h)) 
        
        



class GameOverScreen(GameScreen):
    def __init__(self, w, h):
        super().__init__(w, h)
        
        self.text1 = self.font.render("press SPACE to start", True, 'black')
        self.text_rect1 = self.text1.get_rect(center = (self.w//2, self.h//2))
        self.text2 = self.font.render("press m to go back to menu", True, 'black')
        self.text_rect2 = self.text2.get_rect(center = (self.w//2, self.h//2 + 200))

    def display_bg(self):
        self.screen.fill('white')
        self.screen.blit(self.text1, self.text_rect1)
        self.screen.blit(self.text2, self.text_rect2)
        
        
    def display_score(self, score):
        score_txt = self.font.render(f'score: {score}', True, 'black')
        score_txt_rect = score_txt.get_rect(center = (self.w//2, 200))
        self.screen.blit(score_txt, score_txt_rect)




class Map(GameScreen):

    """
    Klasa mapy

    
    player1 - gracz
    obs - przeszkoda
    game_speed - prędkość gry
    baner - element mapy, kierunek wyspa słodowa
    """

    def __init__(self, w, h):
        super().__init__(w, h)
        self.font = pygame.font.Font("textures/font.ttf", 16)
        self.baner = pygame.image.load('textures/baner.png').convert_alpha()
        self.baner = pygame.transform.rotozoom(self.baner, 0, 0.30) # powinna być na to funkcja
        # i ogólnie elementy mapy pewnie powinny być w jakiejś liście
        self.baner_rect = self.baner.get_rect(center = (self.w - 150, 300))
        self.game_speed = 1 
        self.player1 = Player(350,670) # wstępna pozycja
        self.obstacles = []

        self.game_over = False
        
        self.score = 0

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
        
        
    def display_bg(self):
        # wyświetl tło 
        #self.background = pygame.transform.scale(self.background, (self.w, self.h))

        self.i = 0
        while (self.i < self.tiles):
            self.screen.blit(self.background, (0
                             , self.background.get_height() * -self.i + self.scroll))
            self.i += 1

        self.scroll += 5

        # resetowanie scrolla
        if abs(self.scroll) > self.background.get_height():
            self.scroll = 0
        


    # -------------DEBUG------------------------
    def display_debug_rect(self):
        pygame.draw.rect(self.screen, 'green', self.player1.rect, 2)
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, 'blue', obstacle.rect, 2)




    def display_score(self):
        self.calculate_score()
        self.score_txt = self.font.render(f'score: {self.score}', True, 'gold')
        self.score_txt_rect = self.score_txt.get_rect(topleft = (10, 10))
        self.screen.blit(self.score_txt, self.score_txt_rect)
        
    def increase_speed(self):
        # przyspiesz grę co 3 sekundy -- wartości można zmienić
        if pygame.time.get_ticks() % 300 == 0:
            self.game_speed *= 1.05
            self.player1.dx *= 1.05


    def update_characters(self):
        # update na ekranie pozycję gracza i przeszkód
        # oraz sprawdza kolizję 
        # jeżeli wystąpi kolizja to game_over = True
        self.increase_speed()
        self.add_obstacle()
        self.game_over = self.check_for_obs_collision()
        
        self.update_player()
        self.update_obstacles()
                
    def update_player(self):
        # print(self.check_for_border_collision())
        if self.check_for_border_collision():
            self.player1.move(self.check_for_border_collision())
            self.player1.rect.x = self.player1.x   
            
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

    def add_obstacle(self):
        # dodaje przeszkodę we w miarę losowym momencie, nie może być póki co więcej niż 5 na ekranie
        # sprawdza czy w miejscu gdzie ma się pojawić przeszkoda występuje już jakaś inna przeszkoda
        if random.randint(1, 20) % 19 == 0 and len(self.obstacles) < 5:
            if random.randint(1,11) % 10 == 0:
                obs = StaticObstacle()
            else:
                obs = DynamicObstacle()
            collides = False
            for obstacle in self.obstacles:
                if obs.rect.y <= obstacle.rect.y - 130 or obs.rect.x == obstacle.rect.x:
                    collides = True
                    break
            if collides:
                del obs    
            else:
                self.obstacles.append(obs)
    

    def check_for_obs_collision(self) -> bool:
        # sprawdza czy występuje kolizja gracza z przeszkodą
        for obstacle in self.obstacles:
            if pygame.Rect.colliderect(obstacle.rect, self.player1.rect):
                self.player1.hp -= 1
                self.obstacles.remove(obstacle)
                # self.game_over = True
                return self.checking_hp()

        return False
            

    def display_map_elements(self):
        # wyświetla elementy mapy, takie jak np. baner
        self.screen.blit(self.baner, self.baner_rect)


    def display_characters(self):
        # wyświetla charactery    
        self.player1.display_character(self.screen)
        
        # debug:
        self.display_debug_rect()
        
        for obstacle in self.obstacles:
            obstacle.display_character(self.screen)

    def calculate_score(self):
        # self.score += int((pygame.time.get_ticks() * self.game_speed**10) // 1000)
        self.score += 1


    def is_game_over(self) -> bool:
        return self.game_over

    def checking_hp(self) -> bool:
        if (self.player1.hp == 2):
            print('2')
            self.hp1 = pygame.image.load('textures/kosa.png').convert_alpha()
            self.hp1_rect = self.hp1.get_rect(center=(self.w - 80, self.h - 750))
            self.hp1 = pygame.transform.rotozoom(self.hp1, 0, 0.40)
            return False
        elif (self.player1.hp == 1):
            print('1')
            self.hp2 = pygame.image.load('textures/kosa.png').convert_alpha()
            self.hp2_rect = self.hp2.get_rect(center=(self.w - 40, self.h - 750))
            self.hp2 = pygame.transform.rotozoom(self.hp2, 0, 0.40)
            return False
        elif (self.player1.hp == 0):
            self.hp3 = pygame.image.load('textures/kosa.png').convert_alpha()
            self.hp3_rect = self.hp3.get_rect(center=(self.w, self.h - 750))
            self.hp3 = pygame.transform.rotozoom(self.hp3, 0, 0.40)
            print('deat')
            return True

    def show_life(self):
        self.screen.blit(self.hp1, self.hp1_rect)
        self.screen.blit(self.hp2, self.hp2_rect)
        self.screen.blit(self.hp3, self.hp3_rect)


class Menu(GameScreen):
    def __init__(self, w, h):
        super().__init__(w, h)
        # self.garage_button = pygame.image.load('textures/buttons/butgarage').convert_alpha()
        # self.garage_button_rect = self.garage_button.get_rect(center = (300, 50))
        # self.start_button = pygame.image.load('textures/buttons/butsound').convert_alpha()
        # self.start_button_rect = self.start_button.get_rect(center = (300, 300))
        # self.sound_button = pygame.image.load('textures/buttons/butstart').convert_alpha()
        # self.sound_button_rect = self.sound_button.get_rect(center = (300, 550))

        
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
        self.sceen.blit(self.start_button, self.start_button_rect)
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



class Garage(GameScreen):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.text1 = self.font.render("press m to go back to menu", True, 'black')
        self.text_rect1 = self.text1.get_rect(center = (self.w//2, self.h//2))
        
    def display_garage(self):
        self.screen.fill('brown')
        self.screen.blit(self.text1, self.text_rect1)





