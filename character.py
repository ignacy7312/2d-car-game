import pygame
import random



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
        self.dx = 4

    def move(self, collision):
        if pygame.key.get_pressed()[pygame.K_a] and not collision[0]:
            # jezeli wciska sie 'a' i nie ma kolizji z lewą stroną
            self.x -= self.dx
            self.image = self.turnleft_image
            # self.rect.x = self.turnleft_rect
        elif pygame.key.get_pressed()[pygame.K_d] and not collision[1]:
            # jezeli wciska sie 'd' i nie ma kolizji z prawą stroną
            self.x += self.dx
            self.image = self.turnright_image
            # self.rect = self.turnright_rect
        else:
            # jeżeli auto jedzie prost
            self.image = self.normal_image
            self.rect = self.normal_rect

        
        print(self.rect.width, self.rect.height)
    
    
        

class Obstacle(Character):

    """
    
    Klasa przeszkoda
    Jej obiekty reprezentują przeszkody pojawiające się na ekranie

    Startowe pozycje x,y przeszkód generowane są losowo
    obraz przeszkody (i później jej typ) generowany także losowo
    """

    # lista przeszkód
    obstacle_path_list = ['obstacle1.png', 'obstacle2.png', 'obstacle3.png']

    def __init__(self):
        # konstruktor, nie wymaga argumentów, bo x i y są generowane losowo
        self.x, self.y = self.get_random_position()
        super().__init__(self.x, self.y)
        self.image = pygame.image.load(self.get_obstacle()).convert_alpha()
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.dy = 5

    
    def get_obstacle(self) -> str:
        # zwraca path do losowej przeszkody z listy przeszkód
        return 'textures/' + random.choice(Obstacle.obstacle_path_list)

    def get_random_position(self):
        # zwróć losowe x i y z zakresu (zakres tymczasowy, nie liczyłem pikseli)
        # powinna raczej zwracać wartości z większym skokiem,
        # żeby nie było sytuacji, gdzie przeszkoda pojawia się np na linii oddzielającej pasy
        return random.randint(140, 470), random.randint(0, 100)



    def move(self, multiplier = 1):
        self.y += self.dy * multiplier
        
    