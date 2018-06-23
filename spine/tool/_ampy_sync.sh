
file_name=$dirdalek/micropy/src/main.py
sudo ampy --port /dev/ttyACM0 put ${file}
echo "ampy copied whole src to micropy over serial port"
