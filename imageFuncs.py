# -*- coding: utf-8 -*-
import pygame,math
from pygame.locals import *
import os

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