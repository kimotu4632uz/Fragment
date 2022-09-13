#!/usr/bin/env python
from PIL import Image, ImageDraw
import cv2
import numpy as np

from pathlib import Path

def remove_pad(img, pad_index):
  # ページ中心の余白削除
  remove_pix = 40

  # ページ中心のノイズ削除
  white_pix = 40
  
  if pad_index % 2 == 0:
    img = img.crop((remove_pix, 0, img.width, img.height))
    ImageDraw.Draw(img).rectangle((0, 0, white_pix, img.height), fill=(255,255,255), outline = None)
  else:
    img = img.crop((0, 0, img.width - remove_pix, img.height))
    ImageDraw.Draw(img).rectangle((img.width - white_pix, 0, img.width, img.height), fill=(255,255,255), outline=None)
  
  return img


def remove_noise(img):
  aimg = np.array(img)
  aimg = cv2.cvtColor(aimg, cv2.COLOR_RGB2BGR)
  
  result = cv2.fastNlMeansDenoisingColored(aimg, h=10)
  
  result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
  return Image.fromarray(result)


if __name__ == "__main__":
  # 開始ページの左を消したければ0, 右なら1
  pad_index = 0

  for file in Path.cwd().glob('*.png'):
    with Image.open(file) as img:
      img = remove_pad(img, pad_index)
#      img = remove_noise(img)
      img.save(file.with_stem(file.stem + '_mod'))
    
    pad_index += 1

