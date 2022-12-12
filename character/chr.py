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

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
