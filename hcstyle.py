# -*- coding: utf-8 -*-

import cbg.style

## Typesetting:

BVS = cbg.style.FontFamily('Bitstream Vera Sans', 0.59, 1.1)

LEFT = cbg.style.Type(BVS)
CENTERED_BOLD = cbg.style.Type(BVS, anchor='middle', weight=cbg.style.BOLD)
ITALIC = cbg.style.Type(BVS, style=cbg.style.ITALIC)

ME_TITLE = cbg.style.FontSize(4)
ME_TAGS = cbg.style.FontSize(2.9, after_paragraph_factor=0)
ME_BODY = cbg.style.FontSize(2.9)
ME_FINE = cbg.style.FontSize(2.6)

FONTS_TITLE = { cbg.style.MAIN: CENTERED_BOLD }
FONTS_TAGS = { cbg.style.MAIN: CENTERED_BOLD }
FONTS_BODY = { cbg.style.MAIN: LEFT }
FONTS_FLUFF = { cbg.style.MAIN: ITALIC }

## Color tuples:

BLACK = (cbg.style.COLOR_BLACK,)
WHITE = (cbg.style.COLOR_WHITE,)
GRAY_50 = (cbg.style.COLOR_GRAY_50,)
GREEN = ('#33ee33',)
RED = ('#ee3333',)
YELLOW = ('#eeee33',)
DARKRED = ('#770000',)
SWAMP = ('#44bb88',)
BROWN = ('#aa88888',)
TURQUOISE = ('#2299aa',)

COLORS_BASIC = { cbg.style.MAIN: BLACK
               , cbg.style.ACCENT: TURQUOISE
               , cbg.style.CONTRAST: WHITE
               }

TITLE = cbg.style.Wardrobe(ME_TITLE, FONTS_TITLE, COLORS_BASIC)
TAGS = cbg.style.Wardrobe(ME_TAGS, FONTS_TITLE, COLORS_BASIC)
BODY = cbg.style.Wardrobe(ME_BODY, FONTS_BODY, COLORS_BASIC)
FINE = cbg.style.Wardrobe(ME_FINE, FONTS_FLUFF, COLORS_BASIC)
