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
        if press[K_LEFT]:
            self.rect.move_ip(-self.vx, 0)
        if press[K_RIGHT]:
            self.rect.move_ip(self.vx, 0)
        if press[K_UP]:
            self.rect.move_ip(0, -self.vy)
        if press[K_DOWN]:
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

  
if __name__ == '__main__':
    Game()