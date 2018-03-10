# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import numpy as np

#スクリーンサイズ(px指定)
SCR_RECT = Rect(0, 0, 640, 480)
#マップのサイズ (タテ、ヨコ)
MAP_SIZE = (15, 20)
#背景タイルのサイズ
BG_TILE_SIZE = (32, 32)

#デフォルトの設定
#デフォルトのマップ状態