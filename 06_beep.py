#!/usr/bin/env python
from gpiozero import OutputDevice
from time import sleep

BeepPin = 17  # pin 11

def setup():
    global beep
    beep = OutputDevice(BeepPin)

def loop():
    while True:
        beep.on()   # Beep on
        sleep(0.1)
        beep.off()  # Beep off
        sleep(0.1)

if __name__ == '__main__':
    print('Press Ctrl+C to end the program...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        beep.off()  # Ensure beep is off before exiting
        print('Program stopped.')
