# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (800,600) # スクリーンサイズ（px指定）
#Pygame初期化
pygame.init()
#SCREEN_SIZEの画面作成
screen = pygame.display.set_mode(SCREEN_SIZE)
#タイトルバーの文字セット
pygame.display.set_caption("初めてのシューティング")

#ゲームイベントループ
while True:
    screen.fill((0,0,0)) #画面を真っ青で塗りつぶす
    pygame.display.update() #画面を更新
    #イベント処理
    for event in pygame.event.get():
        if event.type == QUIT: # 終了イベント
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            pressed_keys = pygame.key.get_pressed()
            MyPC.move(pressed_keys)

#キャラを表示したい