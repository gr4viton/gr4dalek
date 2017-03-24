#!/bin/bash
cd /flash/
echo Deleting all *.py from /flash
rm /flash/*.py
echo Copying gr4dalek boot.py to /flash
cp /home/pi/DEV/gr4dalek/micropy/src/boot.py /flash/
echo Done

