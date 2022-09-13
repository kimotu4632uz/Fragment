#!/usr/bin/env python
from pathlib import Path
import io
import sys

from PIL import Image
import img2pdf

imgs = []
outfile = sys.argv[1]

for file in Path.cwd().glob('*.png'):
  img_byte = io.BytesIO()
  with Image.open(file) as img:
    img.save(img_byte, format='JPEG')
  imgs.append(img_byte.getvalue())

Path(outfile).write_bytes(img2pdf.convert(imgs))
