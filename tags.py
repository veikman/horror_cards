# -*- coding: utf-8 -*-

from cbg.tag import Tag as T

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
BALLISTIC = T(VIOLENCE_BALLISTIC, subordinate_to=WOUND)
CUT = T(VIOLENCE_CUT, subordinate_to=WOUND)
BLUNT = T(VIOLENCE_BLUNT, subordinate_to=WOUND)

## Other types of wounds.
DISC = T('discretionary', subordinate_to=WOUND)
TORSO = T('torso', subordinate_to=WOUND)
HEAD = T('head', subordinate_to=WOUND)

## For coloring only.
SUCCESS = T('success', printing=False, subordinate_to=CHECK)
RISK = T('risk', printing=False, subordinate_to=CHECK)
