#!/usr/bin/env python
from gpiozero import DigitalInputDevice
import time
from signal import pause

IrPin=6
count=0
IRrec=DigitalInputDevice(IrPin, pull_up=True)

def cont():
   
    global count
    count +=1
    print("Received infrared. cnt=", count)

"""def loop():
    while True:
        IRrec.when_activated=cont
        #print(IRrec.is_active)
        pause()
        #time.sleep(0.5)"""
        

if __name__ == '__main__': # Program start from here
    try:
        IRrec.when_deactivated=cont
        pause()
    except KeyboardInterrupt: # When 'Ctrl+C' program ended
        print("\n Program ended")   
        IRrec.close()


