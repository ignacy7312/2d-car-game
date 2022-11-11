import pygame
import random
import settings
import math

class Character(pygame.sprite.Sprite):
    """
    
    Klasa Character - dziedziczy po pygame.sprite. 
    Wszystkie klasy obiektów pojawaijących się na ekranie z gry z niej dziedziczą.
    
    Atrybuty:
    x - wstępna pozycja OX
    y - wstępna pozycja na OY
    image, rectangle - parametry wymagane przez pygame.Sprite. Inicjowane do None, bo nie można
    niezdefiniować zmiennej
    
    """

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = None # bo nie można tylko zadeklarować zmiennej
        self.rect = None # j.w.

    def load_and_rescale(self, path : str, scale : float, angle : int = 0 ) -> pygame.image:
            # pobiera path do grafiki, skalę oraz kąt, o jaki ją obraca
            # zwraca przeskalowaną grafikę
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.rotozoom(img, angle, scale)
            return img


    def display_character(self, screen):
        # wyświetl na ekranie
        screen.blit(self.image, self.rect)

    




class Player(Character):
    """

    Klasa Player - gracz (auto)
    Jej obiekt reprezentuje gracza

    Atrybuty:
    game_money - pieniądze zebrane w trakcie jednej gry
    score - wynik uzyskany w trakcie jednej gry
    hp - punkty życia (początkowo 3)
    """

    def __init__(self, x, y):
        # konstruktor, wymaga podania startowej pozycji gracza (auta)
        super().__init__(x, y)
        self.normal_image = self.load_and_rescale('textures/auto.png', 0.22, 180)
        self.normal_rect = self.normal_image.get_rect(center = (self.x, self.y))
        self.turnleft_image = pygame.transform.rotate(self.normal_image, 20)
        # self.turnleft_rect = self.normal_image.get_rect(center = (self.x - 50, self.y))
        # self.turnleft_rect = self.turnleft_image.get_rect(center = (self.x, self.y))
        self.turnright_image = pygame.transform.rotate(self.normal_image, 340)
        # self.turnright_rect = self.normal_image.get_rect(center = (self.x + 50, self.y))
        # self.turnright_rect = self.turnright_image.get_rect(center = (self.x, self.y))
        self.image = self.normal_image
        self.rect = self.normal_rect
        
        # !!!! rect powinien być tylko jeden, nie ma potrzeby na więcej
        
        self.game_money = 0
        self.score = 0
        self.hp = 3
        self.dx = 6

    def move(self, collision):
        if pygame.key.get_pressed()[pygame.K_a] and not collision[0]:
            # jezeli wciska sie 'a' i nie ma kolizji z lewą stroną
            self.x -= int(self.dx)
            self.image = self.turnleft_image
            # self.rect.x = self.turnleft_rect
        elif pygame.key.get_pressed()[pygame.K_d] and not collision[1]:
            # jezeli wciska sie 'd' i nie ma kolizji z prawą stroną
            self.x += int(self.dx)
            self.image = self.turnright_image
            # self.rect = self.turnright_rect
        else:
            # jeżeli auto jedzie prost
            self.image = self.normal_image
            self.rect = self.normal_rect

        
        print(self.rect.width, self.rect.height, self.dx)
    
    
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
        
        return random.choice(Obstacle.obstacle_center_positions), random.randint(-400, 0)



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
        
        