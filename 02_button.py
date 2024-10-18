from gpiozero import LED, Button
from signal import pause

button = Button(27)
led = LED(17)

def led_on(): # Function that runs when the button is pressed to print its status
    print("LED on")

def led_off(): # Function that runs when the button is released to print its status
    print("LED off")

def loop():
    while True:
        # We can use the library's methods for the Button object and call the functions for turning on and off the LED:
        button.when_pressed = led_on
        button.when_released = led_off

        led.source = button # The source attribute of LED class receives te signal from the button to switch between on and off

        pause() # Used to avoid overloading the RPi CPU with continuous data been checked from the button status

def destroy(): # Releases the GPIO pins after the program ends
    button.close()
    led.close()

if __name__ == '__main__': # Program start from here
    try:
        loop()
    except KeyboardInterrupt: # When 'Ctrl+C' is pressed, the childprogram destroy() will be executed.
        destroy()