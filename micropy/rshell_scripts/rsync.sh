#!/bin/bash
rsync -m -v /home/pi/DEV/gr4dalek/micropy/src/ /flash/
#rsync -m -v --exclude={"*.swp"} /home/pi/DEV/gr4dalek/micropy/src/ /media/4621-0000
echo Removing *.swp and *.swo from /flash
rm /flash/*.swp
rm /flash/*.swo
echo Done
