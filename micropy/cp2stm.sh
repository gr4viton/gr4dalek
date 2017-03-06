#/bin/bash
cd /home/pi/DEV/gr4dalek/micropy/
sudo rm /media/4621-0000/main.py
sudo cp main.py servo.py servos_demo.py shared_globals.py boot.py /media/4621-0000/
echo 'copy finished: main, servo, servos_demo, shared_globals, boot'
