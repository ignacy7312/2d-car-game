import pygame
import math
import random

from screen.game_screen_class import GameScreen

class GameOverScreen(GameScreen):
    def __init__(self, w, h):
        super().__init__(w, h)
        
        self.text1 = self.font.render("press SPACE to restart", True, 'black')
        self.text_rect1 = self.text1.get_rect(center = (self.w//2, self.h//2))
        self.text2 = self.font.render("press m to go back to menu", True, 'black')
        self.text_rect2 = self.text2.get_rect(center = (self.w//2, self.h//2 + 200))

    def display_bg(self):
        self.screen.fill('white')
        self.screen.blit(self.text1, self.text_rect1)
        self.screen.blit(self.text2, self.text_rect2)
        
        
    def display_score(self, score):
        score_txt = self.font.render(f'score: {score}', True, 'black')
        score_txt_rect = score_txt.get_rect(center = (self.w//2, 200))
        self.screen.blit(score_txt, score_txt_rect)

    def display_money_earned(self, money):
        money_txt = self.font.render(f'coins earned: ', True, 'black')
        money_txt_rect = money_txt.get_rect(center = (self.w//2, 100))
        coins_txt = self.font.render(f'{money}', True, 'gold')
        coins_txt_rect = coins_txt.get_rect(center = (self.w//2 + 140, 100))
        self.screen.blit(money_txt, money_txt_rect)
        self.screen.blit(coins_txt, coins_txt_rect)
