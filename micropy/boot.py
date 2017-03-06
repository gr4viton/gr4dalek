# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

print('Machine start - boot.py')
import machine
import pyb
try: 
    import pins
    print('pins module imported')
except ImportError:
    print('pins module not found')

pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
#pyb.usb_mode('CDC+HID') # act as a serial device and a mouse
