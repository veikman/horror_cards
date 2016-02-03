# -*- coding: utf-8 -*-

import cbg
import cbg.svg.wardrobe as cw

import hc.tags


# Colors.

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


# Presenter and wardrobe classes.

class CardFront(cbg.svg.card.CardFront):
    class LayoutFromTop(cbg.svg.presenter.FramedLayout):
        Wardrobe = cw.Wardrobe
        cursor_class = cbg.cursor.FromTop

    class LayoutFromBottom(LayoutFromTop):
        cursor_class = cbg.cursor.FromBottom

        def present(self):
            self.cursor.slide(0.5)
            super().present()

    Wardrobe = cbg.sample.wardrobe.Frame
    size = cbg.sample.size.MINI_EURO


class CardBack(cbg.svg.card.CardBack):
    Wardrobe = cbg.sample.wardrobe.Frame
    size = cbg.sample.size.MINI_EURO

    class LayoutFromTop(CardFront.LayoutFromTop):
        def present(self):
            self.cursor.slide(0.3 * self.size[1])
            super().present()


class Title(cbg.svg.presenter.TextPresenter):
    class Wardrobe(cbg.sample.wardrobe.MiniEuroMain):
        modes = {cw.MAIN: cw.Mode(font=cbg.sample.font.BITSTREAM_VERA_SANS,
                                  bold=True, middle=True)}


class Lead(cbg.svg.presenter.TextPresenter):
    class Wardrobe(cbg.sample.wardrobe.MiniEuroSmall):
        modes = {cw.MAIN: cw.Mode(font=cbg.sample.font.BITSTREAM_VERA_SANS)}


class Crunch(cbg.svg.presenter.TextPresenter):
    class Wardrobe(cbg.sample.wardrobe.MiniEuroSmall):
        modes = {cw.MAIN: cw.Mode(font=cbg.sample.font.BITSTREAM_VERA_SANS,
                                  italic=True)}


class RecoveryTime(cbg.svg.presenter.IndentedPresenter):
    Wardrobe = Lead.Wardrobe
    cursor_class = None

    class RecoveryLead(cbg.svg.presenter.SVGPresenter):
        Wardrobe = Lead.Wardrobe

        def present(self):
            self.cursor.slide(1)
            self.insert_paragraph(str(self.field))

    class BoxRow(cbg.svg.presenter.SVGPresenter):
        class Wardrobe(cw.Wardrobe):
            modes = {cw.MAIN: cw.Mode(thickness=0.4, fill_colors=('none',),
                                      stroke_colors=DARKRED)}

        def present(self):
            self.cursor.slide(4.7)
            n_boxes = self.field.content
            for n in range(n_boxes):
                position = self.origin + (0.4 + n * 4.8, self.cursor.offset)
                self.append(cbg.svg.shapes.Rect.new(position, (3.7, 3.7),
                                                    rounding=0.2,
                                                    wardrobe=self.wardrobe))


class Tagbox(cbg.svg.tag.TagBanner):
    class Wardrobe(cbg.sample.wardrobe.MiniEuroSmall):
        modes = {cw.MAIN: cw.Mode(font=cbg.sample.font.BITSTREAM_VERA_SANS,
                                  stroke_colors=BLACK, bold=True, middle=True),
                 cw.INACTIVE: cw.Mode(),
                 cw.BACKGROUND: cw.Mode(stroke_colors=TURQUOISE)}

    cursor_class = None

    def _choose_box_mode(self):
        '''An override.'''
        if not self.field:
            return self.wardrobe.set_mode(cw.INACTIVE)

        self.wardrobe.set_mode(cw.BACKGROUND)

        # Change the wardrobe based on applied tags.
        applied_tags = self.field.card.tags
        if hc.tags.CHECK in applied_tags:
            self.wardrobe.mode.stroke_colors = BLACK
            if hc.tags.SUCCESS in applied_tags:
                self.wardrobe.mode.stroke_colors = GREEN
            if hc.tags.RISK in applied_tags:
                self.wardrobe.mode.stroke_colors = PURPLE
            if hc.tags.SFX_GOOD in applied_tags:
                self.wardrobe.mode.stroke_colors = BLUE
            if hc.tags.SFX_BAD in applied_tags:
                self.wardrobe.mode.stroke_colors = RED
            if hc.tags.WASTE in applied_tags:
                self.wardrobe.mode.stroke_colors = ORANGE
        elif hc.tags.SHOCK in applied_tags:
            self.wardrobe.mode.stroke_colors = YELLOW
        elif hc.tags.INSANITY in applied_tags:
            self.wardrobe.mode.stroke_colors = BROWN
        elif hc.tags.LIFE in applied_tags:
            self.wardrobe.mode.stroke_colors = TURQUOISE
        elif hc.tags.WOUND in applied_tags:
            self.wardrobe.mode.stroke_colors = DARKRED
        else:
            # Back to default. Note we are in fact changing the class, for
            # this presenter type as well as its inheritor.
            self.wardrobe.mode.stroke_colors = BLACK

    def _choose_text_mode(self):
        '''An override.'''
        if not self.field:
            return self.wardrobe.set_mode(cw.INACTIVE)

        self.wardrobe.set_mode(cw.MAIN)

        # Change the wardrobe based on applied tags.
        applied_tags = self.field.card.tags
        if hc.tags.SHOCK in applied_tags:
            self.wardrobe.mode.fill_colors = BLACK
            self.wardrobe.mode.thickness = 0
        else:
            self.wardrobe.mode.fill_colors = WHITE
            self.wardrobe.mode.thickness = 0.02


class StackName(cbg.svg.presenter.SVGPresenter):

    Wardrobe = Title.Wardrobe

    def present(self):
        '''Print a deck name on the back.'''
        applied_tags = self.field.card.tags
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

        self.insert_paragraph(text)
