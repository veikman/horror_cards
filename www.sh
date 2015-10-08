#!/bin/bash -eu
#: Helper for consistent web presentation of the latest version.

W=~/w/games_hc_

for word in check life insanity shock wound
do
  ./init.py -w tag=$word -f ${W}$word.pdf
done

