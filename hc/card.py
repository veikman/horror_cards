# -*- coding: utf-8 -*-
'''Basic card types, slightly more abstract than decks.'''

import cbg

import hc.fields


class BasicCard(cbg.content.card.Card):
    field_classes = hc.fields.BASIC

    presenter_class_front = hc.svg.CardFront
    presenter_class_back = hc.svg.CardBack

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
