# -*- coding: utf-8 -*-

import cbg

import hc.wardrobe
import hc.tags


class CardFront(cbg.svg.presenter.CardFront):
    wardrobe = cbg.sample.wardrobe.WARDROBE
    size = cbg.sample.size.MINI_EURO


class CardBack(cbg.svg.presenter.CardBack):
    wardrobe = cbg.sample.wardrobe.WARDROBE
    size = cbg.sample.size.MINI_EURO


class Title(cbg.svg.presenter.FieldOfText):
    wardrobe = hc.wardrobe.TITLE


class Lead(cbg.svg.presenter.FieldOfText):
    wardrobe = hc.wardrobe.BODY


class Crunch(cbg.svg.presenter.FieldOfText):
    wardrobe = hc.wardrobe.FINE

    def set_up_paragraph(self):
        self.wardrobe.reset()
        self.bottom_up()


class RecoveryTime(cbg.svg.presenter.FieldBase):
    wardrobe = hc.wardrobe.BODY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.content_source:
            # No recovery time.
            return

        lead, boxes = self.content_source

        self.bottom_up()
        self.wardrobe.size = cbg.size.FontSize(7, after_paragraph_factor=0)

        self.insert_text(str(boxes))

        self.wardrobe.reset()
        self.insert_text(str(lead))


class Tagbox(cbg.svg.presenter.FieldBase):
    wardrobe = hc.wardrobe.TAGS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.content_source:
            return
        applied_tags = self.content_source

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

        self.bottom_up()
        self.insert_tagbox(str(applied_tags))


class StackName(cbg.svg.presenter.FieldBase):

    wardrobe = hc.wardrobe.TITLE

    def __init__(self, *args, **kwargs):
        '''Print a deck name on the back.'''
        super().__init__(*args, **kwargs)

        applied_tags = self.content_source.parent.tags
        text = None
        if hc.tags.WOUND in applied_tags:
            for t in applied_tags:
                if t.subordinate_to == hc.tags.WOUND:
                    text = t.full_name
                    break
        else:
            for t in (hc.tags.CHECK, hc.tags.SHOCK,
                      hc.tags.INSANITY, hc.tags.LIFE):
                if t in applied_tags:
                    text = str(t).capitalize()
                    break

        if not text:
            s = 'No label on back side with {}.'
            raise AttributeError(s.format(applied_tags))

        self.insert_text(text)
