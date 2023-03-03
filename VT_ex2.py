from machine import Pin, PWM
import time

pwm_led = PWM(Pin(17, mode=Pin.OUT))

pwm_led.freq(1_000)


while True:
    for i in range(0, 65535, 25000): # on incremente de 1000         
        pwm_led.duty_u16(i) # on lui donne la valeur i         
        time.sleep(0.01) # on attend 0.01 seconde     
    for i in range(65535, 0, -25000): # on decremente de 1000        
        pwm_led.duty_u16(i) # on lui donne la valeur i         
        time.sleep(0.01) # on attend 0.01 seconde
