#!/usr/bin/env python
from gpiozero import PWMLED
import time

led=PWMLED(17, frequency=1e3) #set GPIO and frecuency

def loop():
    while True:
        for dc in range(0,101,4): #increase duty cycle: 0-100
            led.value = dc/100
            time.sleep(0.05)
        time.sleep(1)

        for dc in range(100,-1,-4): # decrease duty cycle: -100-0
            led.value = dc/100
            time.sleep(0.05)
        time.sleep(1)

if __name__ == '__main__': # Program start from here
    try:
        loop()
    except KeyboardInterrupt: # When 'Ctrl+C' program ended
        print("\n Program ended")