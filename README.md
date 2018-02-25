# gr4Dalek
Dalek bot - python @ raspberry pi, micropython @ stm32f4, mecanum drive robot

# will try docker afterwards
[wiringpi docker](https://hub.docker.com/r/acencini/rpi-python-serial-wiringpi/)

## preparations

### rpi setup

Set these:
- camera
- serial 
  - disable system serial console, but enable serial hw
```
$ rpi-config
```
### prerequisities

```
sudo pip install pipenv
```


### connection

#### 2 x L293D - battery 6V
```
```

#### 2 x L293d - 4 x pololu1162 - or the newer
```
```

#### STM32 - 2 x L293D
```
GPIO pins to control the direction and enable
GND
```

#### RPI - STM32
##### GPIO
```
UART
GND
```
##### ports
```
rpi_usb - stm_usb_micro
```


### installation


```
git clone <this-repo-address>

cd py
pipenv install -r req/base.in

```

### run

connect to rpi via ssh
```bash
dalek_me
```
#### rpi sw

get into pipenv venv

```bash
cd $dirdalek/pi
pipenv shell
```

in pipenv-venv 
```bash
python main.py
```

#### stm fw 
see the interactive console of micrpython running on stm from rpi
and sync the filesystem
```
dalek_rshell_rsync
```

# advised aliases

Add this to your `~/.bashrc` and change the `dirdalek` accordingly.
```bash
alias src="source ~/.bashrc"
alias vrc="vim ~/.bashrc"
alias vimrc="vim ~/.vimrc"


# ###############################################
# include dalek bashrc if it exists
export dirdalek="/home/pi/DEV/gr4dalek/"
if [ -f $dirdalek/bashrc ]; then
    . $dirdalek/bashrc
fi
```

The useful aliases are defined in [`bashrc`](bashrc) file.
