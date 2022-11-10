import settings
import pygame
from game_screen_class import *
from sys import exit
import enum

class Game:

    """
    Główna klasa gry
    w,h - rozdzielczość ekranu
    
    """
    pygame.init()
    pygame.display.set_caption('HIGH RIDE')
    
    class State(enum.Enum):
        MENU = 1
        GAME = 2
        GAME_OVER = 3
        GARAGE = 4
    
    
    def __init__(self, w: int, h: int, fps: int):
        self.w = w
        self.h = h
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.game_speed = None
        self.game_over = None
        # po wejsciu do gry jest sie w menu
        self.STATE = Game.State.MENU 
        self.map_screen = None
        self.garage_screen = None
        self.game_over_screen = None
        self.menu_screen = None
        
    def change_state(self):
        # jakas akcja która pozwala zmienić stan - maszyna stanów
        self.change_to_game_from_menu()
        pass
        
    def change_to_game_from_menu(self):
        if self.State == Game.State.MENU and pygame.key.get_pressed()[pygame.K_SPACE]:
            self.State = Game.State.GAME
        
    def change_to_game_from_game_over(self):
        if self.State == Game.State.GAME_OVER and pygame.key.get_pressed()[pygame.K_SPACE]:
            del self.game_screen
            self.game_screen = Map(self.w, self.h)
            self.game_screen.game_over = False
            self.game_over = False
            self.State = Game.State.GAME
    
    def change_to_garage_from_menu(self):
        if self.STATE == Game.State.MENU and pygame.key.get_pressed()[pygame.K_l]:
            self.STATE = Game.State.GARAGE
    
    def change_to_menu_from_garage(self):
        if self.STATE == Game.State.GARAGE and pygame.key.get_pressed()[pygame.K_l]: 
            self.STATE = Game.State.MENU
        
    def change_to_menu_from_game_over(self):
        if self.State == Game.State.MENU and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.STATE = Game.State.MENU
            
    def change_to_game_over_from_game(self):
        if self.State == Game.State.GAME and self.game_over:
            self.STATE = Game.State.GAME_OVER

    def handle_states(self):
        pass
    
    def handle_game_state(self):
        self.game_screen.update_characters()
        self.game_screen.display_bg()
        self.game_screen.display_map_elements()
        self.game_screen.display_characters()
        self.game_screen.display_score()
        
        self.change_to_game_over_from_game()
    
    def handle_game_over_state(self):
        self.menu_screen.display_menu()
        self.menu_screen.display_score(self.game_screen.score)
        self.change_to_game_from_game_over()
        self.change_to_menu_from_game_over()
            
            
    
    def handle_menu_state(self):
        pass
    
    def handle_garage_state(self):
        pass    
    

    def run(self):
        # odpala game loop

        # obiekt mapy: 
        game_screen = Map(self.w, self.h) 
        # obiekt prowizorycznego menu
        game_over_screen = GameOver(self.w, self.h) 
        self.game_over = game_screen.is_game_over()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            # czy game_over
            self.game_over = game_screen.is_game_over()
        
            if not self.game_over:
                game_screen.update_characters()
                game_screen.display_bg()
                game_screen.display_map_elements()
                game_screen.display_characters()
                game_screen.display_score()

            if self.game_over:
                # kiedy się przegra - poki co jedna kolizja z przeszkodą
                game_over_screen.display_menu()
                game_over_screen.display_score(game_screen.score)
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    del game_screen
                    game_screen = Map(self.w, self.h)
                    game_screen.game_over = False


            pygame.display.update()
            self.clock.tick(self.fps)



screen_resolution = (600,800)
SCREEN_WIDTH = screen_resolution[0]
SCREEN_HEIGHT = screen_resolution[1]

def game():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, settings.fps)
    game.run()

if __name__ == '__main__':
    game()



# Na poniższe nie patrzeć, zostaje żeby się nie zgubiło w razie czego
"""resolutuion_option = 1
game_screen_res = settings.screen_resolution[resolutuion_option]
SCREEN_WIDTH = game_screen_res[0]
SCREEN_HEIGHT = game_screen_res[1]
car_scale = settings.car_rescale[resolutuion_option]


# pygame.init()
# ekran = pygame.display.set_mode(game_screen_res)
# pygame.display.set_caption('HIGH RIDE')
# czas = pygame.time.Clock()

# background = pygame.image.load('textures/tlogry.png')
# background = pygame.transform.scale(background, game_screen_res)
# car_surface = pygame.image.load('textures/auto.png')
# car_surface = pygame.transform.rotozoom(car_surface, 180, car_scale)
# car_rectangle = car_surface.get_rect(center = (game_screen_res[0] // 2, game_screen_res[1]  - 50))"""


