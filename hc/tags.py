# -*- coding: utf-8 -*-

from cbg.tag import AdvancedTag


class WoundType(AdvancedTag):
    def __init__(self, specstring):
        name = '{} Wound'.format(specstring.capitalize())
        super().__init__(specstring, full_name=name, subordinate_to=WOUND)


# Mere strings.
VIOLENCE_BALLISTIC = 'ballistic'
VIOLENCE_CUT = 'cut'
VIOLENCE_BLUNT = 'blunt'

# Major tags.
CHECK = AdvancedTag('check')
SHOCK = AdvancedTag('shock')
INSANITY = AdvancedTag('insanity')
WOUND = AdvancedTag('wound')
LIFE = AdvancedTag('life')

# Types of violence.
BALLISTIC = WoundType(VIOLENCE_BALLISTIC)
CUT = WoundType(VIOLENCE_CUT)
BLUNT = WoundType(VIOLENCE_BLUNT)

# Other types of wounds.
DISC = WoundType('discretionary')
TORSO = WoundType('torso')
HEAD = WoundType('head')

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
