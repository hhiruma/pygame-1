# -*- coding: utf-8 -*-
import pygame,math
from pygame.locals import *
import sys
import re
import os

#ゲームの状態
START, PLAY, GAMEOVER = (0, 1, 2)
#方向の状態
DOWN, LEFT, RIGHT, UP = (0, 1, 2, 3)
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
            if(self.key_is_down):
                self.frame += 1  #フレームを1追加する
            self.update()  #情報更新
            self.draw(screen)  #描画更新
            self.key_handler()  #キーハンドラ実行
            pygame.display.update()


    #ゲームオブジェクトを初期化
    def init_game(self):
        #ゲーム状態をSTARTに設定
        self.game_state = START

        #キーが押されているかどうかの判定の初期値をFalseに設定
        #   (押しっぱなしの時のみframeをカウントしてキャラを足踏みさせるのに使う)
        self.key_is_down = False

        #プレイヤーを作成
        self.player = PCSprite("player.png", 4, 4, 400, 500, 5, 5, DOWN, 6)

        #試しに弾も作成
        self.shot = Shot((100, 100))

    #情報の更新
    def update(self):
        self.player.update(self.frame)
        self.shot.update()

    #画面描画
    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.player.draw(screen)
        self.shot.draw(screen)

    #キーハンドラ
    def key_handler(self):
        for event in pygame.event.get():
            if event.type == quit:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                self.key_is_down = True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == KEYUP:
                self.key_is_down = False

        #playerオブジェクトに入力されたキーを渡す
        self.player.move(pygame.key.get_pressed())
        self.shot.move(pygame.key.get_pressed(), self.player)


# キャラクターのスプライトクラス
class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self, filename, iw, ih, x, y, vx, vy, direction, animSpeed):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.imageList = split_image(load_image(filename), 4, 4)
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
            self.direction = RIGHT
            self.rect.move_ip(self.vx, 0)
        if press[K_w]:
            self.direction = UP
            self.rect.move_ip(0, -self.vy)
        if press[K_s]:
            self.direction = DOWN
            self.rect.move_ip(0, self.vy)


#弾のスプライトクラス
class Shot(pygame.sprite.Sprite):
    #弾速
    speed = 20
    def __init__(self, pos):
        # pygame.sprite.Sprite.__init__(self, self.containers)
        self.imageList = split_image(load_image("fire.png"), 8, 2)
        self.image = self.imageList[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos # 中心座標をposに
        self.direction = RIGHT
        self.shooting = False
        self.frame = 0
        self.animSpeed = 3

    def move(self, press, player):
        if press[K_LEFT]:
            self.direction = LEFT
            player.direction = LEFT
            self.rect.center = player.rect.center
            self.shooting = True
        if press[K_RIGHT]:
            self.direction = RIGHT
            player.direction = RIGHT
            self.rect.center = player.rect.center
            self.shooting = True
        if press[K_UP]:
            self.direction = UP
            player.direction = UP
            self.rect.center = player.rect.center
            self.shooting = True
        if press[K_DOWN]:
            self.direction = DOWN
            player.direction = DOWN
            self.rect.center = player.rect.center
            self.shooting = True


    def update(self):
        if self.shooting == True:
            self.frame += 1
            self.image = self.imageList[self.frame/self.animSpeed%4]
            if self.direction == DOWN:
                self.rect.move_ip(0, self.speed)
            if self.direction == LEFT:
                self.rect.move_ip(-self.speed, 0)
            if self.direction == RIGHT:
                self.rect.move_ip(self.speed, 0)
            if self.direction == UP:
                self.rect.move_ip(0, -self.speed)
            # if self.rect.top < 0:
            #     self.kill()
            #     del self

    def draw(self, screen):
        screen.blit(self.image, self.rect)


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


#画像を分割する
def split_image(image, imgRow, imgColumn):
    # @params horizontal: 横方向の画像の数
    # @params vertical: 縦方向の画像の数

    # imgW: 元画像の幅
    # imgH: 元画像の高さ
    imgW = image.get_width()
    imgH = image.get_height()

    # singleImgW: 分割後の画像の幅
    # singleImgH: 分割後の画像の高さ
    singleImgW = imgW / imgRow
    singleImgH = imgH / imgColumn

    # imageListに分割されたイメージのリストが格納される
    imageList = []

    # MEMO: imgHeight と imgWidth　位置逆かもしれない
    # fix this 128
    for i in range(0, imgW, singleImgW):
        for j in range(0, imgH, singleImgH):
            surface = pygame.Surface((singleImgW,singleImgH))
            surface.blit(image, (0,0), (j,i,singleImgW,singleImgH))
            surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
            surface.convert()
            imageList.append(surface)
    return imageList


if __name__ == '__main__':
    Game()