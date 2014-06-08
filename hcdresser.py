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


class RecoveryTime(cbg.svg.SVGField):
    def __init__(self, parent):
        super().__init__(parent, hcstyle.BODY)

    def front(self, tree):
        if not self.parent:
            ## No recovery time.
            return
        self.reset()
        self.bottom_up()
        lead, boxes = self.parent
        self.wardrobe.size = cbg.size.FontSize(7, after_paragraph_factor=0)
        self.insert_text(tree, str(boxes))
        self.wardrobe.reset()
        self.insert_text(tree, str(lead))


class Tagbox(cbg.svg.SVGField):
    def __init__(self, parent):
        super().__init__(parent, hcstyle.TAGS)

    def front(self, tree):
        if not self.parent:
            return
        applied_tags = self.parent[0]

        if tags.CHECK in applied_tags:
            self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.BLACK)
            if tags.SUCCESS in applied_tags:
                self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.GREEN)
            if tags.RISK in applied_tags:
                self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.PURPLE)
            if tags.SFX_GOOD in applied_tags:
                self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.BLUE)
            if tags.SFX_BAD in applied_tags:
                self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.RED)
            if tags.WASTE in applied_tags:
                self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.ORANGE)
        elif tags.SHOCK in applied_tags:
            self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.YELLOW)
            self.wardrobe.colors[cbg.style.CONTRAST] = hcstyle.BLACK
        elif tags.INSANITY in applied_tags:
            self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.BROWN)
        elif tags.LIFE in applied_tags:
            self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.TURQUOISE)
        elif tags.WOUND in applied_tags:
            self.wardrobe = hcstyle.TAGS.but.colors_accent(hcstyle.DARKRED)

        self.reset()
        self.bottom_up()
        self.insert_tagbox(tree, str(applied_tags))

    def back(self, tree):
        '''Print a deck name on the back.'''
        applied_tags = self.parent[0]
        eponymous = (tags.CHECK, tags.SHOCK, tags.INSANITY, tags.LIFE)

        text = None
        if tags.WOUND in applied_tags:
            for t in applied_tags:
                if t.subordinate_to == tags.WOUND:
                    text = t.full_name
                    break
        else:
            for t in eponymous:
                if t in applied_tags:
                    text = str(t).capitalize()
                    break

        if text is None:
            s = 'No label on back side with {}.'
            raise AttributeError(s.format(applied_tags))

        ## Borrow functionality from the Title dresser above.
        cbg.svg.stylist(Title, self.parent, text).front(tree)
