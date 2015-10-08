# -*- coding: utf-8 -*-

import ovid
import cbg

import hc


class Paragraph(cbg.elements.Paragraph):
    def process(self, raw_data):
        markup = ovid.producing.TwoWaySignatureShorthand
        return markup.collective_sub(str(raw_data))


class TitleField(cbg.elements.CardContentField):
    key = cbg.card.HumanReadablePlayingCard.key_title
    presenter_class = hc.svg.Title


class TagField(cbg.tag.AdvancedCardTagField):
    presenter_class = hc.svg.Tagbox


class LeadField(cbg.elements.CardContentField):
    key = 'lead'
    presenter_class = hc.svg.Lead


class CrunchField(cbg.elements.CardContentField):
    key = 'crunch'
    presenter_class = hc.svg.Crunch
    paragraph_class = Paragraph

    def in_spec(self, strings):
        strings = list(cbg.misc.make_listlike(strings))
        applied_tags = self.parent.tags
        if hc.tags.PSYCHOSIS in applied_tags:
            strings.append("When you have as much Psychosis as Cool, "
                           "you can't tell allies from enemies.")
        if hc.tags.BREAKDOWN in applied_tags:
            strings.append('When you have as much Breakdown as Cool, '
                           'you try to kill yourself, or have a heart '
                           'attack.')
        super().in_spec(strings)

    def not_in_spec(self):
        self.in_spec(())


class TimeField(cbg.elements.CardContentField):
    '''A field for ticking off units of time until something happens.'''

    key = 'recovery'
    presenter_class = hc.svg.RecoveryTime

    def in_spec(self, amount):
        unit = 'days'
        maximum_boxes = 8
        if amount > maximum_boxes:
            amount = amount // 7
            unit = 'weeks'
        if amount > maximum_boxes:
            amount = amount // 4
            unit = 'months'
        lead = 'Recovery in {}:'.format(unit)
        super().in_spec((lead, amount * '⬜'))


BASIC = (TitleField,
         TagField,
         LeadField,
         CrunchField,
         TimeField,
         )
