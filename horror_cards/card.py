# -*- coding: utf-8 -*-
'''Basic card types, slightly more abstract than decks.

@author: Viktor Eikman <viktor.eikman@gmail.com>

'''


import cbg

import horror_cards.fields
import horror_cards.svg


class BasicCard(cbg.content.card.Card):
    class FromTop(cbg.content.field.Layout):
        plan = (horror_cards.fields.StackNameField,
                horror_cards.fields.TitleField,
                horror_cards.fields.TagField,
                horror_cards.fields.CrunchField,
                horror_cards.fields.TimeField
                )
        presenter_class_front = horror_cards.svg.CardFront.LayoutFromTop
        presenter_class_back = horror_cards.svg.CardBack.LayoutFromTop

    class FromBottom(cbg.content.field.Layout):
        plan = (horror_cards.fields.FluffField,
                )
        presenter_class_front = horror_cards.svg.CardFront.LayoutFromBottom

    plan = (FromTop, FromBottom)
    presenter_class_front = horror_cards.svg.CardFront
    presenter_class_back = horror_cards.svg.CardBack

    @property
    def _sorting_signature(self):
        '''Salient properties in a combination unique to the card.'''
        tag_values = sum([t.sorting_value for t in self.tags])
        subset = filter(lambda t: not t.subordinate_to, self.tags)
        tag_names = str(sorted(map(str, subset)))

        return (str(self.deck), tag_values, tag_names, str(self))
