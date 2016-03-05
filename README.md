## A graphics generator for Horror Cards

This Python 3 application, `horror_cards`, is an implementation of
[CBG](https://github.com/veikman/cbg) and
[Ovid](https://github.com/veikman/ovid) for drawing the graphics needed
to play a table-top (analog) role-playing game named
[Horror Cards](http://viktor.eikman.se/article/horror-cards).

The application is provided free of charge to enable players of the
game to print copies and make modifications in accordance with the
Creative Commons license of the game.

### Usage

Though it generates graphics, the program contained in this repository
does not have a graphical user interface.

To use it, first install a Python 3 interpreter, CBG and Ovid, and their
3rd-party dependencies. If that's Greek, find a geek.

Then, on your command line, move to the directory of this code
repository and call `init.py`, either as an executable or through
your interpreter, to generate a basic form of the graphics package inside
a local directory named `svg`. Apply the `-h` flag for informaton about
options such as paper size, duplex formatting and intermediate PDF output.

#### Artwork

This repository is just for code. The reverse side of each card refers to
raster artwork files, which are not included. Download them from
[here](http://viktor.eikman.se/gallery/horror-cards-raster-artwork/) into
a subdirectory of `svg`, named `raster_inclusion`.

### Legal

The information presented by the graphics generated with this application
are part of Horror Cards, the game. That game is licensed as
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode).

The application as such is instead licensed as detailed in the
accompanying file COPYING.txt.

