#!/bin/bash
set -e
mk(){ cat > r$1-transcript.md <<EOT
# ROUND $1 — THE CELLAR
EOT
for n in bass guitar cello toypiano; do echo "### $n:"; cat r$1-$n.txt; echo; done >> r$1-transcript.md; }
mk 1
for n in cello guitar toypiano bass; do python3 jam.py 2 $n r2-$n.txt; done; mk 2
for n in bass guitar cello toypiano; do python3 jam.py 3 $n r3-$n.txt; done; mk 3
echo ALLDONE
