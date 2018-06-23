#!/bin/bash
cd /home/pi/DEV/gr4dalek/micropy/
#sudo rm /media/4621-0000/main.py
awk -F, '{$2=$2+1;print}' OFS=, src/version.txt > tmp & mv tmp src/version.txt
echo "VERSION="`cat src/version.txt`

clear_it=0
while getopts "c" opt; do
    case "$opt" in
    c)
        clear_it=1
        ;;
    esac
done


rm /home/pi/DEV/gr4dalek/micropy/src/.*swp

if [ "$clear_it" = 0 ]; then
    echo Normal rsync
    rshell -f rshell_scripts/rsync.sh
else
    echo Clear contents and rsync afterwards
    rshell -f rshell_scripts/clear_and_copy_boot.sh
    rshell -f rshell_scripts/rsync.sh
fi

sync

sleep 2

./connect.sh
