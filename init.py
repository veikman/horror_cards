#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''A minimal adaptation of CBG's template application to Horror Cards.

Call this module on your command line to draw the graphics needed to
play the game.

This project began on 2014-03-28.

@author: Viktor Eikman <viktor.eikman@gmail.com>

'''

# This file is part of a graphics generator for the Horror Cards RPG.
#
# The generator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The generator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the generator.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2014-2016 Viktor Eikman


import os

import cbg

import horror_cards


def main():
    # Move to project folder and make sure there's a place for specifications.
    os.chdir(os.path.dirname(__file__))
    folder_specs = 'specs'
    try:
        os.mkdir(folder_specs)
    except FileExistsError:
        pass

    # Generate specifications for some of the cards.
    for bodymap in (horror_cards.location.Blunt,
                    horror_cards.location.Cut,
                    horror_cards.location.Ballistic):
        bodymap().specification(folder_specs)

    # Use the same basic card type for everything, including manual specs.
    decks = {filename_base: horror_cards.card.BasicCard
             for filename_base in horror_cards.tags.SPECFILES}

    # Execute.
    app = cbg.app.Application('Horror Cards', decks, folder_specs=folder_specs)
    return app.execute()


if __name__ == '__main__':
    status = main()
    exit(status)
