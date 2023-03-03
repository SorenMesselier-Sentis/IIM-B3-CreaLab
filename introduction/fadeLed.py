from machine import Pin, PWM
import time

pinNumberBlue = 22

pwmBlue = PWM(Pin(pinNumberBlue, mode=Pin.OUT))
pwmBlue.freq(1_000)

while True:

    for i in range(0, 20000, 5000) :
        pwmBlue.duty_u16(i)
        time.sleep(0.5)
    for i in range(20000, 0, -5000) :
        pwmBlue.duty_u16(i)
        time.sleep(0.5)
