# -*- coding: utf-8 -*-
import pygame
import random
from pygame.locals import *

from CharacterSpriteClass import CharacterSprite
from ShotClass import Shot
from imageFuncs import load_image, split_image
from constVals import *

#敵のスプライトクラス
class ECSprite(CharacterSprite):
    def move(self):
        num = random.random() * 4
        if num < 1:
            self.direction = LEFT
            self.rect.move_ip(-self.moveSpeed, 0)
        elif num < 2:
            self.direction = RIGHT
            self.rect.move_ip(self.moveSpeed, 0)
        elif num < 3:
            self.direction = UP
            self.rect.move_ip(0, -self.moveSpeed)
        else:
            self.direction = DOWN
            self.rect.move_ip(0, self.moveSpeed)

    def shoot(self):
        pass