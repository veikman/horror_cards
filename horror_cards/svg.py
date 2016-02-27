# -*- coding: utf-8 -*-
'''SVG presenters used by card content managers.

@author: Viktor Eikman <viktor.eikman@gmail.com>

'''


import cbg
import cbg.svg.wardrobe as cw

import horror_cards.tags


# Colors.

BLACK = (cbg.sample.color.BLACK,)
WHITE = (cbg.sample.color.WHITE,)

SEMANTIC = {horror_cards.tags.SUCCESS: ('#33aa33',),
            horror_cards.tags.RISK: ('#297d8a',),
            horror_cards.tags.SFX_GOOD: ('#4549ff',),
            horror_cards.tags.SFX_BAD: ('#bb3333',),
            horror_cards.tags.WASTE: ('#666666',),
            horror_cards.tags.DESPERATION: ('#773377',),
            horror_cards.tags.SHOCK: ('#f7d482',),
            horror_cards.tags.INSANITY: ('#c9bda7',),
            horror_cards.tags.LIFE: ('#a2ac5f',),
            horror_cards.tags.WOUND: ('#770000',),
            }


# Presenter and wardrobe classes.

class CardFront(cbg.svg.card.CardFront):
    class LayoutFromTop(cbg.svg.presenter.FramedLayout):
        Wardrobe = cw.Wardrobe
        cursor_class = cbg.cursor.FromTop

    class LayoutFromBottom(LayoutFromTop):
        cursor_class = cbg.cursor.FromBottom

        def present(self):
            self.cursor.slide(1.2)
            super().present()

    size = cbg.sample.size.MINI_EURO


class CardBack(cbg.svg.card.CardBack):
    size = cbg.sample.size.MINI_EURO

    class LayoutFromTop(CardFront.LayoutFromTop):
        def present(self):
            self.cursor.slide(0.3 * self.size[1])

            super().present()

    def present(self):
        '''Apply raster art in the shape of the front of the card.

        This does not use self.wardrobe.

        '''

        applied_tags = self.field.tags
        filename = None

        tag_map = {horror_cards.tags.CHECK.key: 'check.jpg',
                   horror_cards.tags.SHOCK.key: 'shock.jpg',
                   horror_cards.tags.INSANITY.key: 'insanity.jpg',
                   horror_cards.tags.LIFE.key: 'life.jpg',
                   horror_cards.tags.BALLISTIC.key: 'wound_ballistic.jpg',
                   horror_cards.tags.CUT.key: 'wound_cut.jpg',
                   horror_cards.tags.BLUNT.key: 'wound_blunt.jpg',
                   horror_cards.tags.DISC.key: 'wound_discretionary.jpg',
                   horror_cards.tags.TORSO.key: 'wound_torso.jpg',
                   horror_cards.tags.HEAD.key: 'wound_head.jpg',
                   }

        for tag in applied_tags:
            filename = tag_map.get(tag.key, filename)

        if not filename:
            s = 'No image with {}.'
            raise AttributeError(s.format(applied_tags))

        folder = r'raster_inclusion/'
        filename = folder + filename

        r = CardFront.Wardrobe.modes[cw.MAIN].thickness  # Match front.
        shape = cbg.svg.shapes.Rect.new(self.origin, self.size,
                                        rounding=1.5 * r)
        clip = cbg.svg.misc.ClipPath.new(children=(shape,))
        self.define(clip)
        id_ = 'url(#{})'.format(clip.get('id'))
        art = cbg.svg.misc.Image.new(self.origin, self.size, filename,
                                     clip_path=id_)
        self.append(art)

        self.recurse()


class Title(cbg.svg.presenter.TextPresenter):
    class Wardrobe(cbg.sample.wardrobe.MiniEuroMain):
        modes = {cw.MAIN: cw.Mode(font=cbg.sample.font.BITSTREAM_VERA_SANS,
                                  bold=True, middle=True)}


class Fluff(cbg.svg.presenter.TextPresenter):
    class Wardrobe(cbg.sample.wardrobe.MiniEuroSmall):
        modes = {cw.MAIN: cw.Mode(font=cbg.sample.font.BITSTREAM_VERA_SANS,
                                  italic=True)}


class Crunch(cbg.svg.presenter.TextPresenter):
    class Wardrobe(cbg.sample.wardrobe.MiniEuroSmall):
        modes = {cw.MAIN: cw.Mode(font=cbg.sample.font.BITSTREAM_VERA_SANS)}


class RecoveryTime(cbg.svg.presenter.SVGPresenter):
    Wardrobe = Crunch.Wardrobe
    cursor_class = None

    class RecoveryLead(cbg.svg.presenter.TextPresenter):
        Wardrobe = Crunch.Wardrobe

    class BoxRow(cbg.svg.presenter.IndentedPresenter):

        indentation = cbg.misc.Compass(1, 1)

        class Wardrobe(cw.Wardrobe):
            modes = {cw.MAIN:
                     cw.Mode(thickness=0.4, fill_colors=('none',),
                             stroke_colors=SEMANTIC[horror_cards.tags.WOUND])}

        def present(self):
            n_boxes = self.field.content
            for n in range(n_boxes):
                position = self.origin + (0.4 + n * 4.8, self.cursor.offset)
                self.append(cbg.svg.shapes.Rect.new(position, (3.7, 3.7),
                                                    rounding=0.2,
                                                    wardrobe=self.wardrobe))
            self.cursor.slide(4.7)


class Tagbox(cbg.svg.tag.TagBanner):
    class Wardrobe(cbg.sample.wardrobe.MiniEuroSmall):
        modes = {cw.MAIN: cw.Mode(font=cbg.sample.font.BITSTREAM_VERA_SANS,
                                  stroke_colors=BLACK, bold=True, middle=True),
                 cw.INACTIVE: cw.Mode(),
                 cw.BACKGROUND: cw.Mode(stroke_colors=BLACK)}

    cursor_class = None

    def _choose_line_mode(self, _):
        '''An override.'''
        if not self.field:
            return self.wardrobe.set_mode(cw.INACTIVE)

        self.wardrobe.set_mode(cw.BACKGROUND)

        # Change the wardrobe based on applied tags.
        applied_tags = self.field.tags
        for tag in applied_tags:
            try:
                self.wardrobe.mode.stroke_colors = SEMANTIC[tag]
            except KeyError:
                continue
            else:
                return

        s = 'No color for tags "{}".'
        raise ValueError(s.format(tuple(map(str, applied_tags))))

    def _choose_text_mode(self, _):
        '''An override.'''
        if not self.field:
            return self.wardrobe.set_mode(cw.INACTIVE)

        self.wardrobe.set_mode(cw.MAIN)

        # Change the wardrobe based on applied tags.
        applied_tags = self.field.tags
        if horror_cards.tags.SHOCK in applied_tags:
            self.wardrobe.mode.fill_colors = BLACK
            self.wardrobe.mode.thickness = 0
        else:
            self.wardrobe.mode.fill_colors = WHITE
            self.wardrobe.mode.thickness = 0.02


class StackName(Tagbox, cbg.svg.presenter.IndentedPresenter):
    '''White text on black, based on tags and therefore on Tagbox.

    Indented to show more of the raster card art.

    '''

    indentation = cbg.misc.Compass(0, 1.5)

    class Wardrobe(cw.Wardrobe):
        modes = {cw.MAIN: cw.Mode(font=cbg.sample.font.BITSTREAM_VERA_SANS,
                                  fill_colors=WHITE, bold=True, middle=True),
                 cw.BACKGROUND: cw.Mode(stroke_colors=BLACK)}
        font_size = 4.5

    def present(self):
        applied_tags = self.field.tags
        text = None
        if horror_cards.tags.WOUND in applied_tags:
            for t in applied_tags:
                if t.subordinate_to == horror_cards.tags.WOUND:
                    text = t.full_name
                    break
        else:
            for t in (horror_cards.tags.CHECK, horror_cards.tags.SHOCK,
                      horror_cards.tags.INSANITY, horror_cards.tags.LIFE):
                if t in applied_tags:
                    text = str(t).capitalize()
                    break

        if not text:
            s = 'No label on back side with {}.'
            raise AttributeError(s.format(applied_tags))

        self._insert_banner_line(text)
        self._insert_banner_text(text)

    def _choose_line_mode(self, _):
        '''An override.'''
        self.wardrobe.set_mode(cw.BACKGROUND)

    def _choose_text_mode(self, _):
        self.wardrobe.set_mode(cw.MAIN)
