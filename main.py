# -*- coding: utf-8 -*-
import pygame,math
from pygame.locals import *
import sys
import re
import os
from multiprocessing import Queue
import threading

from PCSpriteClass import PCSprite
from ECSpriteClass import ECSprite
from ShotClass import Shot
from imageFuncs import load_image, split_image, draw_bg
from constVals import *
from config import *

#メインのGameオブジェクト
class Game:
    def __init__(self):
        #各種読み込み
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("初めてのシューティング")

        #Gameオブジェクトの初期化
        self.init_game()

        #メインループ開始
        clock = pygame.time.Clock()
        self.frame = 0
        while True:
            clock.tick(60)  #ループ更新
            if(self.key_is_down):
                self.frame += 1  #フレームを1追加する
                #プレイヤーが動くと（プレイヤーに何か入力があると）敵も動くようにした
                self.enemy.move()
            self.update()  #情報更新
            self.draw(screen)  #描画更新
            pygame.display.update()
            self.key_handler()  #キーハンドラ実行


    #ゲームオブジェクトを初期化
    def init_game(self):
        #ゲーム状態をSTARTに設定
        self.game_state = START

        #キーが押されているかどうかの判定の初期値をFalseに設定
        #   (押しっぱなしの時のみframeをカウントしてキャラを足踏みさせるのに使う)
        self.key_is_down = False

        #プレイヤーを作成
        self.player = PCSprite("player.png", 400, 250, 5, 6, DOWN)

        #敵を作成，一応enemy.pngを用意したがサイズが合わず断念
        self.enemy = ECSprite("player.png", 200, 250, 5, 6, DOWN)

        #背景タイルリスト
        self.img_list = [
            load_image('bg/white_tile.png'),
            load_image('bg/black_tile.png'),
            load_image('bg/red_tile.png')
        ]

        #背景状態
        self.bg_map = np.array([
        #    1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #1
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #2
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #3
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #4
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #5
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #6
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #7
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #8
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #9
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #10
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #11
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #12
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #13
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #14
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #15
        ])

        #背景処理用のQueueオブジェクト
        self.bg_queue = Queue()

    #情報の更新
    def update(self):
        #プレイヤー関連の情報を更新
        self.player.update(self.frame)
        self.player.shotGroup.update(self.bg_map, self.bg_queue)

        #敵関連の情報を更新
        self.enemy.update(self.frame)

        #キューの中身を取り出す
        while not self.bg_queue.empty():
            #座標(coord)をbg_queueから1つ取り出す
            coord = self.bg_queue.get()
            #スレッドを一つ立てて、コールバックにShotクラスのクラスメソッドfireBgEffectを渡してスタートさせる
            # 　@params coord: 座標
            #   @params self.bg_map: 操作対象のmapデータ
            t = threading.Thread(target=Shot.fireBgEffect, args=(coord, self.bg_map))
            t.start()

    #画面描画
    def draw(self, screen):
        screen.fill((0, 0, 0))
        #画面遷移の仕組み
        if self.game_state == START:
            #とりあえずのタイトル
            #fontオブジェクトの作成
            sysfont = pygame.font.SysFont(None, 80)
            #テキストのレンダリング
            moji = sysfont.render("START", False, (255,0,0))
            #表示
            screen.blit(moji, (300,270))
        if self.game_state == PLAY:
            #実際のゲーム画面で更新するものはここ
            draw_bg(screen, self.img_list, self.bg_map)
            self.player.draw(screen)
            self.player.shotGroup.draw(screen)
            self.enemy.draw(screen)
        if self.game_state == GAMEOVER:
            #一旦省略
            pass

    #キーハンドラ
    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    #spaceで画面遷移するようにした
                elif event.key == K_SPACE:
                    if self.game_state == START:
                        self.game_state = PLAY
                    elif self.game_state == GAMEOVER:
                        self.game_state = START
                self.key_is_down = True
            elif event.type == KEYUP:
                self.key_is_down = False

        #playerオブジェクトに入力されたキーを渡す
        self.player.move(pygame.key.get_pressed())
        self.player.shoot(pygame.key.get_pressed())


if __name__ == '__main__':
    Game()