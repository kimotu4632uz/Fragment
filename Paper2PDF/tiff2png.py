#!/usr/bin/env python
import itertools
from pathlib import Path

from PIL import Image

for file in itertools.chain(Path.cwd().glob('*.tiff'), (Path.cwd().glob('*.tif'))):
  with Image.open(file) as img:
    img.save(file.with_suffix('.png'), dpi=img.info['dpi'])
  file.unlink()
