# -*- coding: utf-8 -*-

import cbg

import hcstyle
import tags

class Title(cbg.svg.SVGField):
    def __init__(self, parent):
        super().__init__(parent, hcstyle.TITLE)

class Lead(cbg.svg.SVGField):
    def __init__(self, parent):
        super().__init__(parent, hcstyle.BODY)

class Crunch(cbg.svg.SVGField):
    def __init__(self, parent):
        super().__init__(parent, hcstyle.FINE)

    def set_up_paragraph(self):
        self.wardrobe.reset()
        self.bottom_up()

class Tagbox(cbg.svg.SVGField):
    def __init__(self, parent):
        super().__init__(parent, hcstyle.TAGS)

    def __call__(self, tree):
        if not self.parent:
            return
        applied_tags = self.parent[0]

        if tags.CHECK in applied_tags:
            self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.BLACK)
            if tags.SUCCESS in applied_tags:
                self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.GREEN)
            if tags.RISK in applied_tags:
                self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.RED)
        if tags.SHOCK in applied_tags:
            self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.YELLOW)
            self.wardrobe.colors[cbg.style.CONTRAST] = hcstyle.BLACK
        if tags.INSANITY in applied_tags:
            self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.BROWN)
        if tags.LIFE in applied_tags:
            self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.TURQUOISE)
        if tags.WOUND in applied_tags:
            self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.DARKRED)

        self.wardrobe.reset()
        self.bottom_up()
        self.insert_tagbox(tree, str(applied_tags))
