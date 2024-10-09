#!/usr/bin/env python
from gpiozero import LED
import time
pins = [20, 17, 27, 22, 6, 13, 19, 21  ] #numbers GPIos, for example: gpio17 is 17

def loop():
    while True:
        for pin in pins:
            led= LED(pin) #Set pins in output mode
            led.on() #set +3.3V to on led
            time.sleep(0.5)
            led.off() # off led



if __name__ == '__main__': # Program start from here
    try:
        loop()
    except KeyboardInterrupt: # When 'Ctrl+C' program ended
        print("\n Program ended")