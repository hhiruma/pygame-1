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
        self.player = PCSprite("player.png", 400, 500, 5, 6, DOWN)

    #情報の更新
    def update(self):
        #プレイヤー関連の情報を更新
        self.player.update(self.frame)
        self.player.shotGroup.update()

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
            self.player.draw(screen)
            self.player.shotGroup.draw(screen)
        if self.game_state == GAMEOVER:
            #一旦省略
            pass

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


# キャラクターのスプライトクラス
class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, moveSpeed, animRate, direction):
        pygame.sprite.Sprite.__init__(self)

        #キャラ本体の見た目の初期設定
        self.imageList = split_image(load_image(filename), 4, 4)
        self.image = self.imageList[0]
        self.rect = Rect(x, y, self.image.get_width(), self.image.get_height())

        #キャラの移動関連
        self.moveSpeed = moveSpeed
        self.direction = direction
        self.animRate = animRate

        #射撃関連
        self.shotGroup = pygame.sprite.RenderUpdates()
        self.shooting = False

    def update(self, frame):
        #画面からはみ出さないようにする
        self.rect = self.rect.clamp(SCR_RECT)
        #[animRate]回に1回 imageをimagelistから更新する
        self.image = self.imageList[self.direction*4+frame/self.animRate%4]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


#プレイヤーのスプライトクラス
class PCSprite(CharacterSprite):
    def move(self, press):
        if press[K_a]:
            self.direction = LEFT
            self.rect.move_ip(-self.moveSpeed, 0)
        if press[K_d]:
            self.direction = RIGHT
            self.rect.move_ip(self.moveSpeed, 0)
        if press[K_w]:
            self.direction = UP
            self.rect.move_ip(0, -self.moveSpeed)
        if press[K_s]:
            self.direction = DOWN
            self.rect.move_ip(0, self.moveSpeed)

    def shoot(self, press):
        #矢印キーが押されたらshotオブジェクトを新たに生成
        if press[K_LEFT] or press[K_RIGHT] or press[K_UP] or press[K_DOWN]:
            #すでに「矢印ボタンを長押し中」でなかったら if文内を実行
            if not self.shooting:
                self.shooting = True  #「矢印ボタン長押し中」に設定

                #スコープをif文内に制限してshotオブジェクトを作成
                shot = Shot(self.rect.center, "fire.png")

                #弾を動かし始める（PCSpriteオブジェクトを引数として渡す）
                shot.move(press, self)

                #キャラクターのスプライトのshotGroup（スプライトグループ）に追加
                self.shotGroup.add(shot)
        else:
            #矢印以外を押していたら「矢印ボタン長押し中」を解除
            self.shooting = False


#弾のスプライトクラス
class Shot(pygame.sprite.Sprite):
    def __init__(self, pos, filename):
        pygame.sprite.Sprite.__init__(self)

        #弾本体の見た目の初期設定
        self.imageList = split_image(load_image(filename), 8, 2)
        self.image = self.imageList[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos # 中心座標をposに

        #弾の移動関連
        self.direction = RIGHT
        self.speed = 20
        self.animRate = 3
        self.frame = 0

    def move(self, press, player):
        #打ち始めはプレイヤーと座標を被らせる
        self.rect.center = player.rect.center

        #矢印キーを押したら2つの方向を同時に変化させる
        #    self.direction : 撃つ方向
        #    player.direction : キャラが向く方向
        if press[K_LEFT]:
            self.direction = player.direction = LEFT
        if press[K_RIGHT]:
            self.direction = player.direction = RIGHT
        if press[K_UP]:
            self.direction = player.direction = UP
        if press[K_DOWN]:
            self.direction = player.direction = DOWN


    def update(self):
        #フレームを更新
        self.frame += 1
        #[animRate]回に1回 imageをimagelistから更新する
        self.image = self.imageList[self.frame/self.animRate%4]

        #初期化時に設定したスピードで弾を動かす
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