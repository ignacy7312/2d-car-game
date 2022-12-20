import pygame
from enum import Enum

import settings
from db.storagedriver import StorageDriver
from screen import menu_module, garage_module, game_over_module, map_module, stats_module


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
        STATS = 5
    
    
    def __init__(self, w, h):
        # początkowym stanem programu jest MENU
        self.w = w
        self.h = h
        self.curr_state = GameState.State.MENU
        self.curr_state_obj = None
        #self.game_active_obj = None
        #self.game_over_obj = None
        #self.garage_obj = None
        #self.menu_obj = None
    
    # obie medtody występują w każdej klasie stanu.
    def handle(self): pass
    def get_next_state(self): pass

"""
Klasa GameAgent zajmuje się przejściem między stanami w programie
oraz wykonaniem akcji aktualnie obowiązującego stanu 

także dziedziczy po GameState, zawiera obiekty wszystkich stanów

"""
class GameAgent(GameState):
    
    SELECTED_PLAYER = 0
    highscore = 0
    monety = 0
    cars = 0
    selected_car = 0

    def __init__(self, w, h):
        super().__init__(w, h)
        #self.garage_obj = GarageState(self.w, self.h)
        #self.game_active_obj = GameActiveState(self.w, self.h, garage_module.Garage.SELECTED_CAR)
        #self.game_over_obj = None
        #self.menu_obj = MenuState(self.w, self.h)

        self.storage_driver = StorageDriver()
        self.curr_state_obj = MenuState(self.w, self.h) # pierwotnym stanem jest menu

        self.selected_player = self.storage_driver.get_current_car()



    def change_state(self, next_state : GameState.State):
        # funckja przyjmuje jako argument kolejny stan, który ma nastąpić 
        # i zmienia aktualny stan na kolejny
        if next_state == GameState.State.MENU:               
            self.selected_player = self.storage_driver.get_current_car()
            self.curr_state_obj = MenuState(self.w, self.h)
            self.curr_state = GameState.State.MENU
        
        if next_state == GameState.State.GAME:
            
            self.curr_state_obj = GameActiveState(self.w, self.h, self.selected_player)
            self.curr_state = GameState.State.GAME
        
        if next_state == GameState.State.GAME_OVER:
            self.storage_driver.update_games_played()
            self.curr_state_obj = GameOverState(self.w, self.h, self.curr_state_obj.game_screen.score,
                                                    self.curr_state_obj.game_screen.player1.game_money) #,self.database)
            self.curr_state = GameState.State.GAME_OVER
            
        if next_state == GameState.State.GARAGE:
            self.curr_state_obj = GarageState(self.w, self.h)
            self.curr_state = GameState.State.GARAGE
            
        if next_state == GameState.State.STATS:
            self.curr_state_obj = StatsScreenState(self.w, self.h)
            self.curr_state = GameState.State.STATS
        
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
    def __init__(self, w, h, selected_player):
        super().__init__(w,h)
        self.game_screen = map_module.Map(self.w, self.h, selected_player)
        self.curr_state = GameState.State.GAME

    def handle(self):
        # aktualizuje rozgrywkę
        self.game_screen.update_characters()
        self.game_screen.display_bg()
        #self.game_screen.display_map_elements()
        self.game_screen.display_characters()
        self.game_screen.display_score_and_money()
        self.game_screen.life.show_life(self.game_screen.screen)
        
        

    def get_next_state(self) -> GameState.State:
        # jeżeli warunek zostaje spełniony, to zwraca kolejny stan - wtym wypadku tylko game over
        if self.curr_state == GameState.State.GAME and self.game_screen.game_over:

            return GameState.State.GAME_OVER
        return None

    def reset(self):
        # resetuje rozgrywkę tworząc obiekt mapy na nowo
        self.game_screen = map_module.Map(self.w, self.h)
        
        
"""
Klasa stanu GameOver
tworzy obiekt ekranu GameOver

Ze stanu GameOver można przejść do stanu Menu albo GameActive (rozpocząć rozgrywkę od nowa)

jako argument przyjmuje także wynik uzyskany w poprzedniej grze
"""
class GameOverState(GameActiveState):
    def __init__(self, w, h, score, money):
        super().__init__(w, h, GameAgent.SELECTED_PLAYER) # self.selected_player)
        self.game_over_screen = game_over_module.GameOverScreen(self.w, self.h) 
        self.curr_state = GameState.State.GAME_OVER
        self.score = score
        self.money = money


    def handle(self):

        self.game_over_screen.display_bg()
        self.game_over_screen.display_score(self.score)
        self.game_over_screen.display_money_earned(self.money)
    
        

    def get_next_state(self) -> GameState.State:
        # rozpocznij grę na nowo
        if self.curr_state == GameState.State.GAME_OVER and pygame.key.get_pressed()[pygame.K_SPACE]:
            self.save_hs()
            self.save_money()
            return GameState.State.GAME

        #zmień na stan menu 
        if self.curr_state == GameState.State.GAME_OVER and pygame.key.get_pressed()[pygame.K_m]:
            self.save_hs()
            self.save_money()
            return GameState.State.MENU
        return None

    
    def save_hs(self):
        if self.score > self.game_over_screen.high_score:
            self.storage_driver = StorageDriver(score=self.score)
    
    
    def save_money(self):
        self.storage_driver = StorageDriver(coins=self.money)

"""
Klasa stanu menu.
Poki co nic nie robi oprócz wyświetlenia się i umożliwienia przejścia 
do stanu gry aktywnej lub do garażu

"""
class MenuState(GameState):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.curr_state = GameState.State.MENU
        self.menu_screen = menu_module.Menu(self.w, self.h)
        

    def handle(self):
        self.menu_screen.display_menu_bg()
        self.menu_screen.display_buttons()
        

    def get_next_state(self) -> GameState.State:
        # zmień na grę aktywną
        if self.curr_state == GameState.State.MENU and (self.menu_screen.click_button() == 2 or pygame.key.get_pressed()[pygame.K_SPACE]):
            return GameState.State.GAME

        # zmień na garaż
        if self.curr_state == GameState.State.MENU and self.menu_screen.click_button() == 4:
            return GameState.State.GARAGE
        
        # zmień na garaż
        if self.curr_state == GameState.State.MENU and self.menu_screen.click_button() == 5:
            return GameState.State.STATS
        
        return None
        
"""
Klasa stanu garaż.
Poki co nic nie robi oprócz wyświetlenia się i umożliwienia przejścia 
z powrotem do menu

"""
class GarageState(GameState):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.curr_state = GameState.State.GARAGE
        self.garage_screen = garage_module.Garage(self.w, self.h)
    

    def handle(self):
        self.garage_screen.display_garage()
        self.garage_screen.display_buttons()
        self.garage_screen.move_arrow()
        self.garage_screen.display_car()
        self.garage_screen.select_car() 
        self.garage_screen.unlock_car()


    def get_next_state(self) -> GameState.State:
        # zmień na menu
        if self.curr_state == GameState.State.GARAGE and self.garage_screen.click_menu_button() == 1:
            return GameState.State.MENU
        return None
    
"""
Klasa stanu ekranu statystyk
"""
class StatsScreenState(GameState):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.curr_state = GameState.State.STATS
        self.stats_screen = stats_module.StatsScreen(self.w, self.h)
        
    

    def handle(self):

        self.stats_screen.display()
        self.stats_screen.display_buttons()


    def get_next_state(self) -> GameState.State:
        # zmień na menu
        if self.curr_state == GameState.State.STATS and self.stats_screen.click_menu_button() == 1:
            return GameState.State.MENU
        return None
    