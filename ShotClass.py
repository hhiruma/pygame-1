# -*- coding: utf-8 -*-
import pygame,math
from pygame.locals import *
import time

from imageFuncs import load_image, split_image
from constVals import *
from config import *

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


    def update(self, bg_map, bg_queue):
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

        #自分の座標取得
        map_x = self.rect.centerx
        map_y = self.rect.centery
        self_x = int(map_x / BG_TILE_SIZE[0])
        self_y = int(map_y / BG_TILE_SIZE[1])

        #プレイヤーが端にいるときの弾の配列超えエラーを防ぐ（）
        if 15 <= self_y:
            self_y -= 1
        elif 20 <= self_x:
            self_x -= 1

        #自分の座標に対してscreenのmapの値が0だったら2に変更して燃えるエフェクトにする
        if bg_map[self_y][self_x] == 0:
            bg_map[self_y][self_x] = 2
            #キューに登録する
            bg_queue.put((self_x, self_y))

        #上下左右超えた弾を消す
        if self.rect.bottom < 0 or self.rect.top > SCR_RECT.bottom or self.rect.right < 0 or self.rect.left > SCR_RECT.right:
            self.kill()
            del self

        #mapの値が1の座標になったら消す
        if bg_map[self_y][self_x] == 1:
            self.kill()
            del self

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    #ファイアー様の背景処理ようのコールバック関数
    @classmethod
    def fireBgEffect(self, tmp, bg_map):
        time.sleep(1)
        bg_map[tmp[1]][tmp[0]] = 0