#!/bin/bash -e

# requires imagemagick and img2pdf

mogrify -trim +repage *.png
img2pdf -o out.pdf --rotation=ifvalid *.png

