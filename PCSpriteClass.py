# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

from CharacterSpriteClass import CharacterSprite
from ShotClass import Shot
from imageFuncs import load_image, split_image
from constVals import *

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