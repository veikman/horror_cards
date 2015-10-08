# -*- coding: utf-8 -*-

import cbg


# Typesetting:

BVS = cbg.style.FontFamily('Bitstream Vera Sans', 0.59, 1.1)

LEFT = cbg.style.Type(BVS)
CENTERED_BOLD = cbg.style.Type(BVS, anchor='middle', weight=cbg.style.BOLD)
ITALIC = cbg.style.Type(BVS, style=cbg.style.ITALIC)

FONTS_TITLE = {cbg.style.MAIN: CENTERED_BOLD}
FONTS_TAGS = {cbg.style.MAIN: CENTERED_BOLD}
FONTS_BODY = {cbg.style.MAIN: LEFT}
FONTS_FLUFF = {cbg.style.MAIN: ITALIC}

# Color tuples:

BLACK = (cbg.sample.color.BLACK,)
WHITE = (cbg.sample.color.WHITE,)

RED = ('#bb3333',)
ORANGE = ('#ee8833',)
YELLOW = ('#eeee33',)
GREEN = ('#33aa33',)
BLUE = ('#333388',)
PURPLE = ('#773377',)

DARKRED = ('#770000',)
SWAMP = ('#44bb88',)
BROWN = ('#aa8888',)
TURQUOISE = ('#2299aa',)

COLORS_BASIC = {cbg.style.MAIN: BLACK,
                cbg.style.ACCENT: TURQUOISE,
                cbg.style.CONTRAST: WHITE}

TITLE = cbg.style.Wardrobe(cbg.sample.size.FONT_TITLE_ME,
                           FONTS_TITLE, COLORS_BASIC)
TAGS = cbg.style.Wardrobe(cbg.sample.size.FONT_TAGS_ME,
                          FONTS_TITLE, COLORS_BASIC)
BODY = cbg.style.Wardrobe(cbg.sample.size.FONT_BODY_ME,
                          FONTS_BODY, COLORS_BASIC)
FINE = cbg.style.Wardrobe(cbg.sample.size.FONT_FINEPRINT_ME,
                          FONTS_FLUFF, COLORS_BASIC)
