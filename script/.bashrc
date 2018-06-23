
export raspicam_DIR="/usr/local/lib/cmake/"

alias ffmpeg="avconv"
export LD_LIBRARY_PATH="/usr/local/lib/"
alias wup="sudo ifup wlan0"
alias wdn="sudo ifdown wlan0"
alias wifi_toggle="sudo ifdown wlan0 && sudo ifup wlan0"
alias wifi_vim_wpa_supplicant="sudo vim /etc/wpa_supplicant/wpa_supplicant.conf"
alias wifi_vim_etc_network_interfaces="sudo vim /etc/network/interfaces"

export robot_cv_DIR="/home/pi/.netbeans/remote/192.168.1.159/pcdavidek-Windows-x86_64/D/DEV/CPP/kambot_cv/dist/Debug/GNU-Linux/"

alias cd_robot_cv="cd $robot_cv_DIR"
alias robot_cv=$robot_cv_DIR"kambot_cv"


alias stream_rpicam_video=''
alias stream_it="mjpg_streamer -i \"input_file.so -f /home/pi/stream/ -n out.mjpg\" -o \"output_http.so -w /usr/local/www -p 8080\""
#alias stream_it="mjpg_streamer -i \"$LD_LIBRARY_PATH\input_file.so -f /home/pi/stream/ -n out.mjpg\" -o \"output_http.so -w /usr/local/www -p 8080\""

export dirdalek="/home/pi/DEV/gr4dalek/"
alias cdstmdalek="cd /media/4621-0000/"
alias cdmdalek="cd "$dirdalek"micropy/src"
alias cdpdalek="cd "$dirdalek"py/"
alias vimdalek="vim "$dirdalek"micropy/src/main.py"
alias vipdalek="vim "$dirdalek"py/main.py"
alias vipdalekjoy="vim "$dirdalek"py/cli_gui.py"
alias cpmdalek_all="sudo "$dirdalek"micropy/all_cp2stm.sh"


alias dalek="sudo python3 "$dirdalek"py/main.py"
#alias dalek="python3 "$dirdalek"py/main.py"

alias dalek_rshell_rsync="sudo "$dirdalek"micropy/_rshell_rsync.sh"
alias dalek_rshell_rsync_no="sudo "$dirdalek"micropy/connect.sh"
alias dalek_rshell_rsync_clear="sudo "$dirdalek"micropy/_rshell_rsync.sh -c"

#alias dalek_rsync="sudo "$dirdalek"micropy/rshell_scripts/rsync.sh"
alias dalekAmpy_copy="sudo "$dirdalek"micropy/_ampy_sync.sh"

alias repl="minicom -D /dev/ttyACM0"
# not safe as mmcblk0p1 was boot not stm.
#alias mount_stm="sudo mount /dev/mmcblk0p1 /media/4621-0000/"

alias umount_stm="sudo umount -A /dev/mmcblk0p1"

export dirflask=$dirdalek"flask/"
alias cdfdalek="cd "$dirflask
alias fladalek="sudo python3 "$dirflask"app.py"
alias vifdalek="vim "$dirflask"app.py"
alias dalek_stream="sudo mjpg_streamer -i \"input_file.so -f /home/pi/stream/ -n out.mjpg\" -o \"output_http.so -w /usr/local/www -p 80\""

alias mjpg_reboot_stream="sudo lsof -i :8080 | grep \"mjpg_stre\" | cut -d \" \" -f2 | sudo xargs kill -9"
alias dalek_reboot_stream="sudo lsof -i :80 | grep \"python3\" | cut -d \" \" -f2 | sudo xargs kill -9"

# mjpg_streamer
LD_LIBRARY_PATH='/usr/local/lib'

alias src="source ~/.bashrc"
alias vrc="vim ~/.bashrc"
alias vimrc="vim ~/.vimrc"

echo 'LOADED gr4dalek bashrc!'
