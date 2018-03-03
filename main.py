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
#キャラクターのスプライト（クラス）を作る
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


#プレイヤーのスプライト（クラス）を作る
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

class Shot(pygame.sprite.Sprite):
    #弾
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

class Enemy(pygame.sprite.Sprite):
    #エネミークラス
    speed = 3 # 移動速度

    def __init__(self):
        #初期化処理
        #敵は上からランダムに出てくる
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(SCR_RECT.width - self.rect.width)
        self.rect.bottom = SCR_RECT.top
    def update(self):
        #更新処理
        #ランダムに動き回る
        #上，右，下，左の順に設定
        mov_vec = [(-3 * self.speed, 0),(0, 5 * self.speed), (3 * self.speed, 0)]
        self.rect.move_ip(random.choice(mov_vec))

def load_image(filename, colorkey=None):
    # 画像をロード
    # colorkeyは背景色

    # 画像ファイルがpngかgifか判定するための正規表現
    filecase = re.compile(r'[a-zA-Z0-9_/]+¥.png|[a-zA-Z0-9_/]+¥.gif')

    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image: " + filename)
        raise SystemExit from message

    #画面の拡張子によって処理を振り分け
    is_match = filecase.match(filename)
    if is_match:
        image = image.convert_alpha()
    else:
        image = image.convert()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image
