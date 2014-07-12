# -*- coding: utf-8 -*-

from cbg.tag import Tag as T


class WoundType(T):
    def __init__(self, specstring):
        name = '{} Wound'.format(specstring.capitalize())
        super().__init__(specstring, full_name=name, subordinate_to=WOUND)
        T.all_.append(self)


## Mere strings.
VIOLENCE_BALLISTIC = 'ballistic'
VIOLENCE_CUT = 'cut'
VIOLENCE_BLUNT = 'blunt'

## Major tags.
CHECK = T('check')
SHOCK = T('shock')
INSANITY = T('insanity')
WOUND = T('wound')
LIFE = T('life')

## Types of violence.
BALLISTIC = WoundType(VIOLENCE_BALLISTIC)
CUT = WoundType(VIOLENCE_CUT)
BLUNT = WoundType(VIOLENCE_BLUNT)

## Other types of wounds.
DISC = WoundType('discretionary')
TORSO = WoundType('torso')
HEAD = WoundType('head')

## Minor tags.
STRAIN = T('strain')
PSYCHOSIS = T('psychosis')
BREAKDOWN = T('breakdown')
TORMENT = T('torment', printing=False)

## For coloring only.
SUCCESS = T('success', printing=False, subordinate_to=CHECK)
RISK = T('risk', printing=False, subordinate_to=CHECK)
SFX_GOOD = T('sfx good', printing=False, subordinate_to=CHECK)
SFX_BAD = T('sfx bad', printing=False, subordinate_to=CHECK)
WASTE = T('waste', printing=False, subordinate_to=CHECK)
