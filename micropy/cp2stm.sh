#/bin/bash
cd /home/pi/DEV/gr4dalek/micropy/src
#sudo rm /media/4621-0000/main.py
awk -F, '{$1=$1+1}1' OFS=, version.txt >tmp & mv tmp version.txt
echo "VERSION="`cat version.txt`
sudo cp main.py /media/4621-0000/
sudo cp shared_globals.py /media/4621-0000/
sudo cp boot.py /media/4621-0000/
sudo cp version.txt /media/4621-0000/
echo 'copy finished: main, shared_globals, boot, version'
