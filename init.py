#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''A utility for the card graphics needed to play Horror Cards.

Project began on 2014-03-28.

@author: Viktor Eikman <viktor.eikman@gmail.com>

'''

import cbg

import horror_cards


DECKS = {'basic': horror_cards.card.BasicCard,
         horror_cards.location.FILENAME: horror_cards.card.BasicCard}


def main():
    app = cbg.app.Application('Horror Cards', DECKS)
    horror_cards.location.generate(app.folder_specs)
    return app.execute()


if __name__ == '__main__':
    status = main()
    exit(status)
