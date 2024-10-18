from gpiozero import LED    # import gpiozero
from time import sleep		# import time library
led = LED(17)
def loop():
    while True:
        print('...led on')
        led.on()			# turn ON LED
        sleep(1)			# wait 1 second
        print('led off...')
        led.off()			# turn OFF LED
        sleep(1)			# wait 1 second

def destroy(): #Turns off the LED and releases the GPIO pin after the program ends
    led.off()
    led.close()
    
if __name__ == '__main__': # Program start from here
    try:
        loop()
    except KeyboardInterrupt: # When 'Ctrl+C' is pressed, the childprogram destroy() will be executed.
        destroy()