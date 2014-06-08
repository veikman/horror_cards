#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''A utility for the card graphics needed to play Horror Cards.

Project began on 2014-03-28.

@author: Viktor Eikman <viktor.eikman@gmail.com>

'''

import cbg

import cardtypes
import location

DECKS = {'basic': cardtypes.BasicCard,
         location.FILENAME: cardtypes.BasicCard}

## TODO: weapons
## TODO: bizarre wound types
## TODO: stat cards, skill cards


def main():
    app = cbg.app.Application('Horror Cards', DECKS)
    location.generate('yaml')
    app.execute()
    return 0

if __name__ == '__main__':
    status = main()
    exit(status)
