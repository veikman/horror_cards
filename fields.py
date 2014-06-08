# -*- coding: utf-8 -*-

from cbg.elements import CardContentField as F
from cbg.tag import Tag as T
import cbg.card
import cbg.tag
import cbg.elements
import cbg.exc

import hcdresser


class Time(F):
    '''A field for ticking off units of time until something happens.'''
    def fill(self, days):
        amount = days
        unit = 'days'
        maximum_boxes = 8
        if amount > maximum_boxes:
            amount = amount // 7
            unit = 'weeks'
        if amount > maximum_boxes:
            amount = amount // 4
            unit = 'months'
        lead = 'Recovery in {}:'.format(unit)
        super().fill((lead, amount * '⬜'))


TITLE = F(cbg.card.TITLE, hcdresser.Title)
TAGS = cbg.tag.FieldOfTags('tags', hcdresser.Tagbox, T.all_)
LEAD = F('lead', hcdresser.Lead)
CRUNCH = F('crunch', hcdresser.Crunch)
RECOVERY = Time('recovery', hcdresser.RecoveryTime)

BASIC = ( TITLE
        , TAGS
        , LEAD
        , CRUNCH
        , RECOVERY
        )
