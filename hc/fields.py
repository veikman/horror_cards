# -*- coding: utf-8 -*-

import ovid
import cbg

import hc


class _OvidParagraph(cbg.content.text.Paragraph):
    @classmethod
    def format_text(cls, raw_data):
        markup = ovid.producing.TwoWaySignatureShorthand
        return markup.collective_sub(str(raw_data))


class TitleField(cbg.content.text.TextField):
    key = cbg.content.card.Card.key_title
    presenter_class_front = hc.svg.Title


class TagField(cbg.content.tag.AdvancedTagField):
    presenter_class_front = hc.svg.Tagbox


class FluffField(cbg.content.text.TextField):
    key = 'fluff'
    presenter_class_front = hc.svg.Fluff


class CrunchField(cbg.content.text.TextField):
    key = 'crunch'
    presenter_class_front = hc.svg.Crunch
    plan = [_OvidParagraph]

    def in_spec(self):
        self.specification = list(cbg.misc.make_listlike(self.specification))

        applied_tags = self.tags

        if hc.tags.PSYCHOSIS in applied_tags:
            self.specification.append("When you have as much Psychosis as "
                                      "Cool, you can't tell allies from "
                                      "enemies.")

        if hc.tags.BREAKDOWN in applied_tags:
            self.specification.append("When you have as much Breakdown as "
                                      "Cool, you try to kill yourself or "
                                      "have a heart attack.")

        super().in_spec()

    def not_in_spec(self):
        self.specification = []
        self.in_spec()


class TimeField(cbg.content.field.Layout):
    '''A field for ticking off units of time until something happens.'''

    key = 'recovery'
    presenter_class_front = hc.svg.RecoveryTime

    class TimeAmount(cbg.content.field.ArbitraryContainer):
        presenter_class_front = hc.svg.RecoveryTime.BoxRow

    class TimeText(cbg.content.text.TextField):
        presenter_class_front = hc.svg.RecoveryTime.RecoveryLead

    def in_spec(self):
        amount = self.specification
        unit = 'days'
        maximum_boxes = 8
        if amount > maximum_boxes:
            amount = amount // 7
            unit = 'weeks'
        if amount > maximum_boxes:
            amount = amount // 4
            unit = 'months'
        lead = 'Recovery in {}:'.format(unit)

        self.append(self.TimeText(specification=lead, parent=self))
        self.append(self.TimeAmount(specification=amount, parent=self))


class StackNameField(cbg.content.text.TextField):
    presenter_class_back = hc.svg.StackName
