#!/bin/bash
cd /home/pi/DEV/gr4dalek/micropy/
#sudo rm /media/4621-0000/main.py
awk -F, '{$1=$1+1}1' OFS=, src/version.txt >tmp & mv tmp src/version.txt
echo "VERSION="`cat src/version.txt`

rshell -f rshell_scripts/rsync.sh
sync
minicom -D /dev/ttyACM0
