import pygame
import random
import settings
import math

from character.character import Character


class Obstacle(Character):

    """
    Klasa przeszkoda
    Jej obiekty reprezentują przeszkody pojawiające się na ekranie.
    Przeszkody dzielą się na statyczne i dynamiczne

    Startowe pozycje x,y przeszkód generowane są losowo
    obraz przeszkody (i później jej typ) generowany także losowo
    """

    # lista przeszkód dynamicznych
    obstacle_path_list = ['obstacle1.png', 'obstacle2.png', 'obstacle3.png', 'obstacle4.png']
    # lista przeszkód statycznych
    static_obs_path_list = ['carcrash.png'] # , 'pixelwire.png'] 
    # drut wygląda brzydko - do poprawienia
    obstacle_center_positions = settings.lanes_center_list

    def __init__(self):
        # konstruktor, nie wymaga argumentów, bo x i y są generowane losowo
        self.x, self.y = self.get_random_position()
        super().__init__(self.x, self.y)


    def get_random_position(self):
        # zwróć jedną z czterech możliwych pozycji - w środku każdego z pasów ruchu 
        # na wysokości ponad ekranem, żeby był efekt wyjechania przeszkody na ekran,
        # a nie że po prostu się losowo pojawia 
        
        return random.choice(Obstacle.obstacle_center_positions), random.randint(-600, 0)



    def move(self, multiplier = 1):
        self.y += self.dy * multiplier
        
    
class DynamicObstacle(Obstacle):
    def __init__(self):    
        # self.x, self.y = self.get_random_position()
        super().__init__()
        self.image = pygame.image.load(self.get_obstacle()).convert_alpha()
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.dy = 8
        
    def get_obstacle(self) -> str:
        # zwraca path do losowej przeszkody z listy przeszkód
        return 'textures/' + random.choice(Obstacle.obstacle_path_list)
        
    
    
class StaticObstacle(Obstacle):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(self.get_obstacle()).convert_alpha()
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.dy = 5 # wartość równa scrollowi mapy - wtedy wygląda jakby się nie ruszało
        
    def get_obstacle(self) -> str:
        # zwraca path do losowej przeszkody z listy przeszkód
        return 'textures/' + random.choice(Obstacle.static_obs_path_list)   
