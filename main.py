# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import re

#ゲームの状態
START, PLAY, GAMEOVER = (0, 1, 2)
#スクリーンサイズ(px指定)
SCR_RECT = Rect(0, 0, 800, 600)


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
        while True:
            clock.tick(60)  #ループ更新
            self.draw(screen)  #描画更新
            self.key_handler()  #キーハンドラ実行
            pygame.display.update()


    #ゲームオブジェクトを初期化
    def init_game(self):
        #ゲーム状態をSTARTに設定
        self.game_state = START

        #プレイヤーを作成
        self.player = PCSprite("./images/pc_img.png", 400, 500, 3, 3)

    #情報の更新
    def update(self):
        self.player.update()

    #画面描画
    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.player.draw(screen)

    #キーハンドラ
    def key_handler(self):
        for event in pygame.event.get():
            if event.type == quit:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        #playerオブジェクトに入力されたキーを渡す
        self.player.move(pygame.key.get_pressed())


# キャラクターのスプライトクラス
class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = Rect(x, y, width, height)
        self.vx = vx
        self.vy = vy

    def update(self):
        #画面からはみ出さないようにする
        self.rect = self.rect.clamp(SCR_RECT)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


#プレイヤーのスプライトクラス
class PCSprite(CharacterSprite):
    def move(self, press):
        if press[K_a]:
            self.rect.move_ip(-self.vx, 0)
        if press[K_d]:
            self.rect.move_ip(self.vx, 0)
        if press[K_w]:
            self.rect.move_ip(0, -self.vy)
        if press[K_s]:
            self.rect.move_ip(0, self.vy)


#弾のスプライトクラス
class Shot(pygame.sprite.Sprite):
    #弾速
    speed = 9
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos # 中心座標をposに
    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:
            self.kill()
            del self

if __name__ == '__main__':
    Game()