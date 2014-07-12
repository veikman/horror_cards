# -*- coding: utf-8 -*-

from cbg.elements import CardContentField as F
import cbg.card
import cbg.tag
import cbg.elements
import cbg.exc

import hcdresser
import hctags


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


class InterpolatingCrunch(F):
    def fill(self, strings):
        applied_tags = self.parent.tags
        if hctags.PSYCHOSIS in applied_tags:
            strings.append("When you have as much Psychosis as Cool, "
                           "you can't tell allies from enemies.")
        if hctags.BREAKDOWN in applied_tags:
            strings.append('When you have as much Breakdown as Cool, '
                           'you try to kill yourself, or have a heart '
                           'attack.')
        super().fill(strings)

    def not_in_spec(self):
        self.fill([])


TITLE = F(cbg.card.TITLE, hcdresser.Title)
TAGS = cbg.tag.FieldOfTags('tags', hcdresser.Tagbox, cbg.tag.Tag.all_)
LEAD = F('lead', hcdresser.Lead)
CRUNCH = InterpolatingCrunch('crunch', hcdresser.Crunch)
RECOVERY = Time('recovery', hcdresser.RecoveryTime)

BASIC = ( TITLE
        , TAGS
        , LEAD
        , CRUNCH
        , RECOVERY
        )
