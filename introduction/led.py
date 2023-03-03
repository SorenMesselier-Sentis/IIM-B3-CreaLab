from machine import Pin
import time

pinNumberWhite = 17
pinNumberBlue = 22

ledWhite = Pin(pinNumberWhite, mode=Pin.OUT)
ledBlue = Pin(pinNumberBlue, mode=Pin.OUT)

while True:
    ledWhite.toggle()
    time.sleep(1)
    ledWhite.toggle()

    ledBlue.toggle()
    time.sleep(1)
    ledBlue.toggle()