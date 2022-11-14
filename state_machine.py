import pygame
from enum import Enum
import settings
import character
import game_screen_class
import main




"""
Klasa GameState
po niej dziedziczą wszystkie klasy odpowiedzialne za stany w całym programie:
Menu, GameActive, GameOver, Garage

curr_state  - aktualny stan
curr_state_obj - aktualny obiekt danego stanu

Obiekt każdego stanu zajmuje się wykonywaniem akcji tego stanu
"""

class GameState():
    
    class State(Enum):
        MENU = 1
        GAME = 2
        GAME_OVER = 3
        GARAGE = 4
    
    
    def __init__(self, w, h):
        # początkowym stanem programu jest MENU
        self.w = w
        self.h = h
        self.curr_state = GameState.State.MENU
        self.curr_state_obj = None
        self.game_active_obj = None
        self.game_over_obj = None
        self.garage_obj = None
        self.menu_obj = None
    
    # obie medtody występują w każdej klasie stanu.
    def handle(self): pass
    def get_next_state(self): pass

"""
Klasa GameAgent zajmuje się przejściem między stanami w programie
oraz wykonaniem akcji aktualnie obowiązującego stanu 

także dziedziczy po GameState, zawiera obiekty wszystkich stanów

"""
class GameAgent(GameState):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.game_active_obj = GameActiveState(self.w, self.h)
        self.game_over_obj = None
        self.garage_obj = GarageState(self.w, self.h)
        self.menu_obj = MenuState(self.w, self.h)
        self.curr_state_obj = self.menu_obj # pierwotnym stanem jest menu

    def change_state(self, next_state : GameState.State):
        # funckja przyjmuje jako argument kolejny stan, który ma nastąpić 
        # i zmienia aktualny stan na kolejny
        if next_state == GameState.State.MENU:
            self.curr_state_obj = MenuState(self.w, self.h)
        
        if next_state == GameState.State.GAME:
            self.curr_state_obj = GameActiveState(self.w, self.h)
        
        if next_state == GameState.State.GAME_OVER:
            self.curr_state_obj = GameOverState(self.w, self.h, self.curr_state_obj.game_screen.score)
            
        if next_state == GameState.State.GARAGE:
            self.curr_state_obj = GarageState(self.w, self.h)
        
    def execute(self):
        # wykonanie akcji aktualnie obowiązującego stanu
        self.curr_state_obj.handle()
        # sprawdzenie, czy ma nastąpić zmiana stanu
        self.change_state(self.curr_state_obj.get_next_state())


"""
Klasa stanu Game Active (gdy jest się w trakcie gry)

tworzy obiekt mapy, który zajmuje się całą logiką rozgrywki oraz sprawdza, 
czy ma nastąpić przejście do kolejnego stanu. Ze stanu gry aktywnej mozna przejść jedynie do GameOver

"""
class GameActiveState(GameState):
    def __init__(self, w, h):
        super().__init__(w,h)
        self.game_screen = game_screen_class.Map(self.w, self.h)
        self.curr_state = GameState.State.GAME


    def handle(self):
        # aktualizuje rozgrywkę
        self.game_screen.update_characters()
        self.game_screen.display_bg()
        self.game_screen.display_map_elements()
        self.game_screen.display_characters()
        self.game_screen.display_score()
        self.game_screen.show_life()
        
        

    def get_next_state(self) -> GameState.State:
        # jeżeli warunek zostaje spełniony, to zwraca kolejny stan - wtym wypadku tylko game over
        if self.curr_state == GameState.State.GAME and self.game_screen.game_over:
            return GameState.State.GAME_OVER

    def reset(self):
        # resetuje rozgrywkę tworząc obiekt mapy na nowo
        self.game_screen = game_screen_class.Map(self.w, self.h)
        
        
"""
Klasa stanu GameOver
tworzy obiekt ekranu GameOver

Ze stanu GameOver można przejść do stanu Menu albo GameActive (rozpocząć rozgrywkę od nowa)

jako argument przyjmuje także wynik uzyskany w poprzedniej grze
"""
class GameOverState(GameActiveState):
    def __init__(self, w, h, score):
        super().__init__(w, h)
        self.game_over_screen = game_screen_class.GameOverScreen(self.w, self.h) 
        self.curr_state = GameState.State.GAME_OVER
        self.score =  score
        
    def handle(self):

        self.game_over_screen.display_bg()
        self.game_over_screen.display_score(self.score)
    
        

    def get_next_state(self) -> GameState.State:
        # rozpocznij grę na nowo
        if self.curr_state == GameState.State.GAME_OVER and pygame.key.get_pressed()[pygame.K_SPACE]:
            return GameState.State.GAME

        #zmień na stan menu 
        if self.curr_state == GameState.State.GAME_OVER and pygame.key.get_pressed()[pygame.K_m]:
            return GameState.State.MENU



"""
Klasa stanu menu.
Poki co nic nie robi oprócz wyświetlenia się i umożliwienia przejścia 
do stanu gry aktywnej lub do garażu

"""
class MenuState(GameState):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.curr_state = GameState.State.MENU
        self.menu_screen = game_screen_class.Menu(self.w, self.h)
        

    def handle(self):
        self.menu_screen.display_menu_bg()

    def get_next_state(self) -> GameState.State:
        # zmień na grę aktywną
        if self.curr_state == GameState.State.MENU and pygame.key.get_pressed()[pygame.K_SPACE]:
            return GameState.State.GAME

        # zmień na garaż
        if self.curr_state == GameState.State.MENU and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return GameState.State.GARAGE
        
        
"""
Klasa stanu garaż.
Poki co nic nie robi oprócz wyświetlenia się i umożliwienia przejścia 
z powrotem do menu

"""
class GarageState(GameState):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.curr_state = GameState.State.GARAGE
        self.garage_screen = game_screen_class.Garage(self.w, self.h)
    

    def handle(self):
        self.garage_screen.display_garage() 

    def get_next_state(self) -> GameState.State:
        # zmień na menu
        if self.curr_state == GameState.State.GARAGE and pygame.key.get_pressed()[pygame.K_m]: 
            return GameState.State.MENU