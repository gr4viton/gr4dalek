#/bin/bash
cd /home/pi/DEV/gr4dalek/micropy/src
#sudo rm /media/4621-0000/main.py
awk -F, '{$1=$1+1}1' OFS=, version.txt >tmp & mv tmp version.txt
echo "VERSION="`cat version.txt`
sudo cp -r * /media/4621-0000/
sync
watch grep -e Dirty: -e Writeback: /proc/meminfo
#watch -t -n1 'awk "{ print \$9 }" /sys/block/mmcblk0/stat'
echo 'copy finished! *'
