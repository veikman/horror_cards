#!/bin/bash -eu
#: Helper for consistent web presentation of the latest version.

W=~/w/games_hc_

./init.py -w tag=check -f ${W}check.pdf
./init.py -w tag=life -g -f ${W}life.pdf

