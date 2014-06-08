# -*- coding: utf-8 -*-
'''Basic card types, slightly more abstract than decks.'''

import cbg
from cbg.markup import Shorthand as S

import fields


FATALITY = S('FATALITY_CHECK', ('When you gain this: Check Physique minus '
             'your total Strain to stay alive.'))

TOKENS = (FATALITY,)


class BasicCard(cbg.card.HumanReadablePlayingCard):

    @property
    def sorting_keys(self):
        '''An iterable unique to the card type.

        Designed to allow the built-in sorted() function to put the card
        in a good place, relative to others in its deck, for the purpose
        of reading through the deck in electronic form.

        '''
        tag_values = sum([t.sorting_value for t in self.tags])
        subset = filter(lambda t: not t.subordinate_to, self.tags)
        tag_names = str(sorted(map(str, subset)))

        return (tag_values, tag_names, self.title)

    @property
    def tags(self):
        ## Field must exist, so that it can be populated on the basis
        ## of rules etc. on the card.
        return self.field_by_markupstring(fields.TAGS.markupstring)[0]

    def process(self):
        self.dresser = cbg.svg.SVGCard(self, cbg.wardrobe.WARDROBE,
                                       size=cbg.size.MINI_EURO)
        self.populate_fields(fields.BASIC)
        self.substitute_tokens(TOKENS)
