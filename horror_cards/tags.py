# -*- coding: utf-8 -*-
'''Tags for cards.

Tags are used to organize the decks, to control SVG coloring, and for special
rules shared between several cards.

@author: Viktor Eikman <viktor.eikman@gmail.com>

'''


from cbg.content.tag import AdvancedTag


class HCTag(AdvancedTag):
    def __init__(self, specstring, full_name=None, **kwargs):
        full_name = full_name or specstring.capitalize()
        super().__init__(specstring, full_name=full_name, **kwargs)

    def __str__(self):
        return self.key


class WoundType(HCTag):
    def __init__(self, specstring, full_name=None, **kwargs):
        full_name = full_name or '{} Wound'.format(specstring.capitalize())
        super().__init__(specstring, full_name=full_name, subordinate_to=WOUND,
                         **kwargs)


# Mere strings.
VIOLENCE_BALLISTIC = 'ballistic'
VIOLENCE_CUT = 'cut'
VIOLENCE_BLUNT = 'blunt'
VIOLENCE = (VIOLENCE_BALLISTIC, VIOLENCE_CUT, VIOLENCE_BLUNT)

# Major tags.
CHECK = HCTag('check')
SHOCK = HCTag('shock', sorting_value=2)
INSANITY = HCTag('insanity', sorting_value=4)
WOUND = HCTag('wound')
LIFE = HCTag('life', sorting_value=1)

# Types of violence.
BALLISTIC = WoundType(VIOLENCE_BALLISTIC, sorting_value=8)
CUT = WoundType(VIOLENCE_CUT, sorting_value=16)
BLUNT = WoundType(VIOLENCE_BLUNT, sorting_value=32)

# Other types of wounds.
DISC = WoundType('discretionary', sorting_value=64)
TORSO = WoundType('torso', sorting_value=128)
HEAD = WoundType('head', sorting_value=256)

# Minor tags.
STRAIN = HCTag('strain')
PSYCHOSIS = HCTag('psychosis')
BREAKDOWN = HCTag('breakdown')
TORMENT = HCTag('torment', printing=False)

# For coloring only.
SUCCESS = HCTag('success', printing=False, subordinate_to=CHECK)
RISK = HCTag('risk', printing=False, subordinate_to=CHECK)
DESPERATION = HCTag('desperation', printing=False, subordinate_to=CHECK)
SFX_GOOD = HCTag('sfx good', printing=False, subordinate_to=CHECK)
SFX_BAD = HCTag('sfx bad', printing=False, subordinate_to=CHECK)
WASTE = HCTag('waste', printing=False, subordinate_to=CHECK)


# A comprehensive list of the strings which identify decks.
DECKS = (CHECK, SHOCK, INSANITY, LIFE, BALLISTIC,
         CUT, BLUNT, DISC, TORSO, HEAD)
DECK_KEYS = tuple(map(lambda t: t.key, DECKS))
SPECFILES = tuple(map(lambda s: 'auto_' + s if s in VIOLENCE else s,
                      DECK_KEYS))
