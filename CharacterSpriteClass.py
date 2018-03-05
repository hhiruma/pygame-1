# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

from imageFuncs import load_image, split_image
from constVals import *

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