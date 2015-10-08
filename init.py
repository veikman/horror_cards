#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''A utility for the card graphics needed to play Horror Cards.

Project began on 2014-03-28.

TODO: weapons
TODO: bizarre wound types
TODO: stat cards, skill cards

@author: Viktor Eikman <viktor.eikman@gmail.com>

'''

import cbg

import hc


DECKS = {'basic': hc.card.BasicCard,
         hc.location.FILENAME: hc.card.BasicCard}


def main():
    app = cbg.app.Application('Horror Cards', DECKS)
    hc.location.generate(app.folder_specs)
    app.execute()
    return 0

if __name__ == '__main__':
    status = main()
    exit(status)
