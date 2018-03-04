# -*- coding: utf-8 -*-
import pygame,math
from pygame.locals import *
import sys
import re
import os

#ゲームの状態
START, PLAY, GAMEOVER = (0, 1, 2)
#方向の状態
RIGHT, LEFT, DOWN, UP = (0, 1, 2, 3)
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
        self.frame = 0
        while True:
            clock.tick(60)  #ループ更新
            self.frame += 1  #経過フレーム数
            self.update()  #情報更新
            self.draw(screen)  #描画更新
            self.key_handler()  #キーハンドラ実行
            pygame.display.update()


    #ゲームオブジェクトを初期化
    def init_game(self):
        #ゲーム状態をSTARTに設定
        self.game_state = START

        #プレイヤーを作成
        self.player = PCSprite("./images/pc_img.png", 400, 500, 5, 5, DOWN, 6)

    #情報の更新
    def update(self):
        self.player.update(self.frame)

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
    def __init__(self, filename, x, y, vx, vy, direction, animSpeed):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.imageList = split_image(load_image("player.png"))
        self.image = self.imageList[0]
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = Rect(x, y, width, height)
        self.vx = vx
        self.vy = vy
        self.animSpeed = animSpeed

    def update(self, frame):
        #画面からはみ出さないようにする
        self.rect = self.rect.clamp(SCR_RECT)
        self.image = self.imageList[self.direction*4+frame/self.animSpeed%4]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


#プレイヤーのスプライトクラス
class PCSprite(CharacterSprite):
    def move(self, press):
        if press[K_a]:
            self.direction = LEFT
            self.rect.move_ip(-self.vx, 0)
        if press[K_d]:
            self.direction = DOWN
            self.rect.move_ip(self.vx, 0)
        if press[K_w]:
            self.direction = UP
            self.rect.move_ip(0, -self.vy)
        if press[K_s]:
            self.direction = RIGHT
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


def load_image(filename, colorkey=None):
    filename = os.path.join("images", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print("Cannot load image:", filename)
        raise SystemExit, message

    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def split_image(image):
    """128x128のキャラクターイメージを32x32の16枚のイメージに分割
    分割したイメージを格納したリストを返す"""
    GS = 32
    imageList = []
    for i in range(0, 128, GS):
        for j in range(0, 128, GS):
            surface = pygame.Surface((GS,GS))
            surface.blit(image, (0,0), (j,i,GS,GS))
            surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
            surface.convert()
            imageList.append(surface)
    return imageList


if __name__ == '__main__':
    Game()