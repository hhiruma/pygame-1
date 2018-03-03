# -*- coding: utf-8 -*-
import pygame,math
from pygame.locals import *
import sys

START, PLAY, GAMEOVER = (0, 1, 2) #ゲーム状態
SCR_RECT = Rect(0,0,800,600) # スクリーンサイズ（px指定）

class Game:
    def __init__(self):
        #各種読み込み
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("初めてのシューティング")
        #ゲームオブジェクトを初期化
        self.init_game()
        #メインループ開始
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            print('yeah')
            #self.key_handler()


    def init_game(self):
        #ゲームオブジェクトを初期化

        #ゲーム状態
        self.game_state = START


    def update(self):
        pass



    def draw(self,screen):
        #描画
        screen.fill((0, 0, 0))
        if self.game_state == START:
            sysfont = pygame.font.SysFont(None, 80)
            sys = sysfont.render("PUSH SPACE TO START",False,(255,0,0))
            screen.blit(sys, ((SCR_RECT.width-sys.get_width())/2,270))

        if self.game_state == PLAY:
            self.all_sprite.draw(screen)

        if self.game_state == GAMEOVER:
            sysfont = pygame.font.SysFont(None, 80)
            sys = sysfont.render("GAMEOVER",False,(255,0,0))
            screen.blit(sys, ((SCR_RECT.width-sys.get_width())/2,270))







if __name__ == '__main__':
    Game()
