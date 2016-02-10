# -*- coding: utf-8 -*-

from cbg.content.tag import AdvancedTag


class WoundType(AdvancedTag):
    def __init__(self, specstring, **kwargs):
        name = '{} Wound'.format(specstring.capitalize())
        super().__init__(specstring, full_name=name, subordinate_to=WOUND,
                         **kwargs)

    def __str__(self):
        return self.key


# Mere strings.
VIOLENCE_BALLISTIC = 'ballistic'
VIOLENCE_CUT = 'cut'
VIOLENCE_BLUNT = 'blunt'

# Major tags.
CHECK = AdvancedTag('check')
SHOCK = AdvancedTag('shock', sorting_value=2)
INSANITY = AdvancedTag('insanity', sorting_value=4)
WOUND = AdvancedTag('wound')
LIFE = AdvancedTag('life', sorting_value=1)

# Types of violence.
BALLISTIC = WoundType(VIOLENCE_BALLISTIC, sorting_value=8)
CUT = WoundType(VIOLENCE_CUT, sorting_value=16)
BLUNT = WoundType(VIOLENCE_BLUNT, sorting_value=32)

# Other types of wounds.
DISC = WoundType('discretionary', sorting_value=64)
TORSO = WoundType('torso', sorting_value=128)
HEAD = WoundType('head', sorting_value=256)

# Minor tags.
STRAIN = AdvancedTag('strain')
PSYCHOSIS = AdvancedTag('psychosis')
BREAKDOWN = AdvancedTag('breakdown')
TORMENT = AdvancedTag('torment', printing=False)

# For coloring only.
SUCCESS = AdvancedTag('success', printing=False, subordinate_to=CHECK)
RISK = AdvancedTag('risk', printing=False, subordinate_to=CHECK)
SFX_GOOD = AdvancedTag('sfx good', printing=False, subordinate_to=CHECK)
SFX_BAD = AdvancedTag('sfx bad', printing=False, subordinate_to=CHECK)
WASTE = AdvancedTag('waste', printing=False, subordinate_to=CHECK)
