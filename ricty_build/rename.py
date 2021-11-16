#!/usr/bin/env python

import fontforge

f = fontforge.open('Ricty Regular Nerd Font Complete Windows Compatible.ttf')
f.familyname = "RictyNF"
f.fullname = "RictyNF Regular"
f.fontname = "RictyNF-Regular"
f.close()

f = fontforge.open('Ricty Oblique Nerd Font Complete Windows Compatible.ttf')
f.familyname = "RictyNF"
f.fullname = "RictyNF Oblique"
f.fontname = "RictyNF-Oblique"
f.close()

