from machine import Pin
import utime

pinNumber = 12
pinNumber2 = 21
pinNumber3 = 13
led = Pin(pinNumber, mode=Pin.OUT)
led2 = Pin(pinNumber2, mode=Pin.OUT)
led3 = Pin(pinNumber3, mode=Pin.OUT)

while True:
    led.toggle()
    utime.sleep(1)
    led.toggle()
    led2.toggle()
    utime.sleep(1)
    led2.toggle()
    led3.toggle()
    utime.sleep(1) 
    led3.toggle()