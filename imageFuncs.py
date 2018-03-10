# -*- coding: utf-8 -*-
import pygame,math
from pygame.locals import *
import os
import numpy as np
from constVals import *
from config import *

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

#背景描画
def draw_bg(screen, img_list, bg_map):
    #仕様
    #  imgListで背景に使用する画像のリストを受けとる
    #  mapでどの位置に各画像を配置するかを記す行列を渡す（各座標のあたいはimgListの画像のindex）

    #mapのrow、columnを受け取る

    #mapのサイズが定数MAP_SIZEに一致するかの確認
    if not bg_map.shape == MAP_SIZE:
        print('MAP_SIZEと一致しません')
        print(bg_map.shape)
        return

    #imageListのタイルのサイズが定数BG_TILE_SIZEに一致するかの確認
    for image in img_list:
        if not image.get_width == BG_TILE_SIZE[0] and image.get_height == BG_TILE_SIZE[1]:
            print('BG_TILE_SIZEと一致しません')
            return

    map_width = MAP_SIZE[1]
    map_height = MAP_SIZE[0]
    tile_width = BG_TILE_SIZE[0]
    tile_height = BG_TILE_SIZE[1]

    #mapリストに併せて指定画像をscreenに追加していく
    for y in range(0, map_height):
        for x in range(0, map_width):
            screen.blit(img_list[bg_map[y][x]], (tile_width * x, tile_height * y))