import pygame
import random
import settings
import math

from character.chr import Character
from screen.garage_module import Garage


class Player(Character):
    """

    Klasa Player - gracz (auto)
    Jej obiekt reprezentuje gracza

    Atrybuty:
    game_money - pieniądze zebrane w trakcie jednej gry
    score - wynik uzyskany w trakcie jednej gry
    hp - punkty życia (początkowo 3)
    """

    def __init__(self, x, y, selected_car):
        # konstruktor, wymaga podania startowej pozycji gracza (auta) oraz numeru odpowiadającego auta
        super().__init__(x, y)
        self.player_red = self.load_and_rescale('textures/czerwonegora.png', 0.22, 0)
        self.player_yellow = self.load_and_rescale('textures/lambogora.png', 0.22, 0)
        self.player_white = self.load_and_rescale('textures/bialegora.png', 0.22, 0)

        self.normal_image = self.select_player(selected_car)
        self.normal_rect = self.normal_image.get_rect(center = (self.x, self.y))
        self.turnleft_image = pygame.transform.rotate(self.normal_image, 20)
        # self.turnleft_rect = self.normal_image.get_rect(center = (self.x - 50, self.y))
        # self.turnleft_rect = self.turnleft_image.get_rect(center = (self.x, self.y))
        self.turnright_image = pygame.transform.rotate(self.normal_image, 340)
        # self.turnright_rect = self.normal_image.get_rect(center = (self.x + 50, self.y))
        # self.turnright_rect = self.turnright_image.get_rect(center = (self.x, self.y))
        #self.turn_rect = self.normal_image.get_rect(center = (self.x + 90, self.y))
        
        # przezroczysty obraz - 54/110 wymiary auta
        self.blink_image = pygame.Surface((54,110), pygame.SRCALPHA, 32)
        
        self.image = self.normal_image
        self.rect = self.normal_rect
        
        # !!!! rect powinien być tylko jeden, nie ma potrzeby na więcej
        
        self.game_money = 0
        self.score = 0
        self.hp = 3
        self.dx = 6
        self.blink_invinc_end_time = 0
        self.invincible = False
        self.is_colliding = False

    def select_player(self, selected_car) -> pygame.image:
        # wybierz auto zgodnie z numeracja
        print(selected_car)
        if selected_car == 0:
            return self.player_red
        if selected_car == 1:
            return self.player_yellow
        if selected_car == 2:
            return self.player_white


    def move(self, collision):
        if pygame.key.get_pressed()[pygame.K_a] and not collision[0]:
            # jezeli wciska sie 'a' i nie ma kolizji z lewą stroną
            self.x -= int(self.dx)
            self.image = self.turnleft_image
            #self.rect = self.turn_rect
        elif pygame.key.get_pressed()[pygame.K_d] and not collision[1]:
            # jezeli wciska sie 'd' i nie ma kolizji z prawą stroną
            self.x += int(self.dx)
            self.image = self.turnright_image
            #self.rect = pygame.Rect((self.x+100, self.y), (50, 100))
        else:
            # jeżeli auto jedzie prost
            self.image = self.normal_image
            self.rect = self.normal_rect
            
    def display_player(self, image, screen):
        screen.blit(image, self.rect)


        # print(self.rect.width, self.rect.height, self.dx)
    
    
    # cztery punkty - cztery wierzchołki prostokąta obrócone o kąt wobec pivota - środka prostokąta
    """def rotate_by_point(self, cx : int, cy : int, angle : float, point : list(int, int)):
        s = math.sin(angle)
        c = math.cos(angle)
        point[0] -= cx
        point[1] -= cy

        # rotate point
        xnew = point[0] * c - point[1] * s
        ynew = point[0] * s + point[1] * c
        
        point[0] = xnew + cx
        point[1] = ynew + cy 
        
        return point"""
