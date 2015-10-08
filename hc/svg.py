# -*- coding: utf-8 -*-

import cbg

import hc.wardrobe
import hc.tags


class Card(cbg.svg.SVGCard):
    wardrobe = cbg.sample.wardrobe.WARDROBE
    size = cbg.sample.size.MINI_EURO


class Title(cbg.svg.SVGField):
    wardrobe = hc.wardrobe.TITLE


class Lead(cbg.svg.SVGField):
    wardrobe = hc.wardrobe.BODY


class Crunch(cbg.svg.SVGField):
    wardrobe = hc.wardrobe.FINE

    def set_up_paragraph(self):
        self.wardrobe.reset()
        self.bottom_up()


class RecoveryTime(cbg.svg.SVGField):
    wardrobe = hc.wardrobe.BODY

    def front(self, tree):
        if not self.parent:
            # No recovery time.
            return
        self.reset()
        self.bottom_up()
        lead, boxes = self.parent
        self.wardrobe.size = cbg.size.FontSize(7, after_paragraph_factor=0)
        self.insert_text(tree, str(boxes))
        self.wardrobe.reset()
        self.insert_text(tree, str(lead))


class Tagbox(cbg.svg.SVGField):
    wardrobe = hc.wardrobe.TAGS

    def front(self, tree):
        if not self.parent:
            return
        applied_tags = self.parent

        def accent(color):
            self.wardrobe = hc.wardrobe.TAGS.but.colors_accent(color)

        if hc.tags.CHECK in applied_tags:
            accent(hc.wardrobe.BLACK)
            if hc.tags.SUCCESS in applied_tags:
                accent(hc.wardrobe.GREEN)
            if hc.tags.RISK in applied_tags:
                accent(hc.wardrobe.PURPLE)
            if hc.tags.SFX_GOOD in applied_tags:
                accent(hc.wardrobe.BLUE)
            if hc.tags.SFX_BAD in applied_tags:
                accent(hc.wardrobe.RED)
            if hc.tags.WASTE in applied_tags:
                accent(hc.wardrobe.ORANGE)
        elif hc.tags.SHOCK in applied_tags:
            accent(hc.wardrobe.YELLOW)
            self.wardrobe.colors[cbg.style.CONTRAST] = hc.wardrobe.BLACK
        elif hc.tags.INSANITY in applied_tags:
            accent(hc.wardrobe.BROWN)
        elif hc.tags.LIFE in applied_tags:
            accent(hc.wardrobe.TURQUOISE)
        elif hc.tags.WOUND in applied_tags:
            accent(hc.wardrobe.DARKRED)

        self.reset()
        self.bottom_up()
        self.insert_tagbox(tree, str(applied_tags))

    def back(self, tree):
        '''Print a deck name on the back.'''
        applied_tags = self.parent[0]
        eponyms = (hc.tags.CHECK, hc.tags.SHOCK,
                   hc.tags.INSANITY, hc.tags.LIFE)

        text = None
        if hc.tags.WOUND in applied_tags:
            for t in applied_tags:
                if t.subordinate_to == hc.tags.WOUND:
                    text = t.full_name
                    break
        else:
            for t in eponyms:
                if t in applied_tags:
                    text = str(t).capitalize()
                    break

        if text is None:
            s = 'No label on back side with {}.'
            raise AttributeError(s.format(applied_tags))

        # Borrow functionality from the Title dresser above.
        cbg.svg.stylist(Title, self.parent, text).front(tree)
