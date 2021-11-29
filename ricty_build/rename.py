#!/usr/bin/env python3

import fontforge

print('start rename')

src = 'Ricty Regular Nerd Font Complete Windows Compatible.ttf'
dst = 'RictyNF-Regular.ttf'

f = fontforge.open(src)
family = 'RictyNF'
fullname = 'RictyNF Regular'
fontname = 'RictyNF-Regular'

f.familyname = family
f.fullname = fullname
f.fontname = fontname
f.appendSFNTName('English (US)', 'PostScriptName', fontname)
f.appendSFNTName('English (US)', 'Fullname', fullname)
f.appendSFNTName('English (US)', 'Family', family)
f.appendSFNTName('English (US)', 'Preferred Family', family)
f.appendSFNTName('English (US)', 'Compatible Full', fullname)

f.generate(dst, flags=('opentype', 'PfEd-comments'))
f.close()

