# -*- coding: utf-8 -*-
'''String substitution markup.

@author: Viktor Eikman <viktor.eikman@gmail.com>

'''


import ovid


@ovid.producing.TwoWaySignatureShorthand.swallow
def fatality():
    return 'When you gain this: Check Physique minus Strain to stay alive.'


@ovid.producing.TwoWaySignatureShorthand.swallow
def blackout():
    return 'When you gain this: Take 1 Stress or lose consciousness.'
