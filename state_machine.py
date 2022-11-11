import pygame
import enum
import settings
import character
import game_screen_class
import main



class State(enum.Enum):
    MENU = 1
    GAME = 2
    GAME_OVER = 3
    GARAGE = 4


class GameSate(main.Game):
    def __init__(self):
        super()
        # początkowo jest się w menu
        self.curr_state = State.MENU
        self.curr_state_obj = MenuState()

    def change_state(self, next_state : State):
        # funckja przyjmuje jako argument kolejny stan, który ma nastąpić 
        # i zmienia aktualny stan na obiekt tego stanu
        if next_state == State.MENU:
            self.curr_state_obj = MenuState()
        if next_state == State.GAME:
            self.curr_state_obj = GameActiveState()
        if next_state == State.GAME_OVER:
            self.curr_state_obj = GameOverState()
        if next_state == State.GARAGE:
            self.curr_state_obj = GarageState()
        
    def handle_game_states(self):
        self.curr_state_obj.handle()
        next_state = self.curr_state_obj.change_state()

        # jeżeli stan następny jest różny niż aktualny
        if next_state != self.curr_state:
            self.change_state(next_state)

class GameActiveState(GameSate):
    def __init__(self):
        super()
        self.game_screen = Map(self.w, self.h)
        self.game_speed = None
        self.game_over = None

    def handle(self):
        self.game_screen.update_characters()
        self.game_screen.display_bg()
        self.game_screen.display_map_elements()
        self.game_screen.display_characters()
        self.game_screen.display_score()
        
        self.change_to_game_over_from_game()

    def change_state(self):
        # zmień na game_over z game
        if self.State == Game.State.GAME and self.game_over:
            return Game.State.GAME_OVER

        


class GameOverState(GameActiveState):
    def __init__(self):
        super()
        self.game_over_screen = GameOverScreen(self.w, self.h) 
        self.game_over = game_screen.is_game_over()
        
    def handle(self):
        # self.menu_screen.display_menu()
        # self.menu_screen.display_score(self.game_screen.score)
        self.game_over_screen.display_menu()
        self.game_over_screen.display_score(self.game_screen.score)
        self.change_to_game_from_game_over()
        self.change_to_menu_from_game_over()


    def change_state(self):
        # zmień na stan gry aktywnej gdy jest game_over
        if self.State == Game.State.GAME_OVER and pygame.key.get_pressed()[pygame.K_SPACE]:
            del self.game_screen
            self.game_screen = Map(self.w, self.h)
            self.game_screen.game_over = False
            self.game_over = False
            return Game.State.GAME

        # zmień na stan menu gdy jest game over
        if self.State == Game.State.MENU and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            del self.game_screen
            
            return Game.State.MENU













class MenuState(GameState):
    def __init__(self):
        super()
        self.menu_screen = game_screen_class.Menu(self.w, self.h)

    def handle(self):
        pass

    def change_state(self):
        # zmień na grę aktywną z menu
        if self.State == Game.State.MENU and pygame.key.get_pressed()[pygame.K_SPACE]:
            return Game.State.GAME

        # zmień na garaż z menu
        if self.STATE == Game.State.MENU and pygame.key.get_pressed()[pygame.K_l]:
            return Game.State.GARAGE
        
        


class GarageState(GameState):
    def __init__(self):
        super()
        self.garage_screen = game_screen_class.Garage(self.w, self.h)
    
    def handle(self):
        pass    

    def change_state(self):
        # zmień na menu z garażu
        if self.STATE == Game.State.GARAGE and pygame.key.get_pressed()[pygame.K_l]: 
            return Game.State.MENU