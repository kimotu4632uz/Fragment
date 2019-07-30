#!/usr/bin/env python
import sys
from pathlib import Path
import re
from PIL import Image
from PIL.ExifTags import TAGS

def rename_jpeg(path, regex)
    for file in Path(path).iterdir():
    	if not re.match(regex, file.name):
	    	continue
    	else:
            with Image.open(p) as img:
                for k, v in img._getexif().items():
                    if TAGS.get(k) == 'DateTimeOriginal':
                        p.rename(p.with_name(re.sub(':| ', '', v) + p.suffix))


if __name__ == "__main__":
	rename_jpeg('/sdcard/DCIM', ')
	