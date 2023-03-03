from machine import Pin
import time

pin_button = Pin(2, mode=Pin.IN, pull=Pin.PULL_UP)

while True:

    if pin_button : 
        print(pin_button.value())
        time.sleep(.1)
