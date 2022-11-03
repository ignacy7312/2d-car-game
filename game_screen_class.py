import settings
from character import *

import pygame

class GameScreen():

    """
    Klasa po któej dziedziczyć będą pozostałe ekrany, tj Mapa, Garaż czy Menu/Options

    w,h - rozdzielczość ekranu
    screen - odpalenie pokazywania ekranu w pygame

    
    """
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.screen = pygame.display.set_mode((self.w, self.h))
        
        
        

    def display_bg(self):
        # wyświetl tło 
        
        self.background = pygame.transform.scale(self.background, (self.w, self.h))
        self.screen.blit(self.background, (0,0))
        
        


        '''# self.screen.blit(self.car, self.car_rect)
        # self.screen.blit(self.baner, self.baner_rect)
        rescale_background()
        pygame.display.update()'''


    def rescale_background(self):
           self.background = pygame.transform.scale(self.background, (self.w, self.h))
           
            #self.baner = pygame.transform.rotozoom(self.baner,0,self.car_scale)
            #self.baner_rect = self.baner.get_rect(center =(self.w - 250, self.h - 450))


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
        self.background = pygame.image.load('textures/tlogry.png').convert_alpha()
        self.baner = pygame.image.load('textures/baner.png').convert_alpha()
        self.baner = pygame.transform.rotozoom(self.baner, 0, 0.30) # powinna być na to funkcja, ale już mi się nie chce
        # i ogólnie elementy mapy pewnie powinny być w jakiejś liście
        self.baner_rect = self.baner.get_rect(center = (self.w - 150, 300))
        
        self.game_speed = 1

        
        self.player1 = Player(350,700) # wstępna pozycja
        # self.obs = Obstacle() # powinna być lista przeszkód, ale to już dalszy etap
        self.obstacles = []
        
    def increase_speed(self):
        # przyspiesz grę o 1.01 co 3 sekundy -- wartości można zmienić
        if pygame.time.get_ticks() % 300 == 0:
            self.game_speed *= 1.01

    def update_characters(self):
        # funkcja updateująca pozycję na ekranie gracza i przeszkody
        # w momencie kolizji ekran freezuje (wstępnie)
        print(self.game_speed)
        self.increase_speed()
        self.add_obstacle()
        
        # self.obs.move()
        # self.obs.rect.y = self.obs.y
        self.update_player()
        self.update_obstacles()
                
    def update_player(self):
        # print(self.check_for_border_collision())
        if self.check_for_border_collision():
            self.player1.move(self.check_for_border_collision())
            self.player1.rect.x = self.player1.x   
            
    def check_for_border_collision(self) -> list[bool, bool]:
        # zwraca kolizję z granicą w postaci dwuelementowej listy
        # w któej idx 0 oznacza kolizję z lewą granicą drogi
        # a idx 1 oznacza kolizję z prawą granicą drogi
        # jeżeli doda się możliwość przeszkalowania ekranu trzeba też będzie
        # wartości const zmienić na jakieś variable
        if 110 > self.player1.x:
            # kolizja z lewej strony
            return [True, False]
        elif self.player1.rect.left > 380: # or self.player1.rect.right > 490:
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
                if obstacle.y > self.h:
                    # gdy przeszkoda wyjdzie poza ekran jest usuwana z listy i obiekt też jest usuwany
                    self.obstacles.remove(obstacle)
                    del obstacle

    def add_obstacle(self):
        # dodaje przeszkodę we w miarę losowym momencie, nie może być póki co więcej niż 4 na ekranie
        if random.randint(1, 100) % 97 == 0 and len(self.obstacles) < 4:
            self.obstacles.append(Obstacle())        

    def check_for_collision(self) -> bool:
        # sprawdza czy występuje kolizja gracza z przeszkodą
        for obstacle in self.obstacles:
            if pygame.Rect.colliderect(obstacle.rect, self.player1.rect):
                return True
            

    def display_map_elements(self):
        # wyświetla elementy mapy, takie jak np. baner
        self.screen.blit(self.baner, self.baner_rect)


    def display_characters(self):
        # wyświetla charactery    
        self.player1.display_character(self.screen)
        # self.player1.display_player_turning(self.screen)
        # self.obs.display_character(self.screen)
        for obstacle in self.obstacles:
            obstacle.display_character(self.screen)

    
