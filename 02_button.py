from gpiozero import LED, Button
from signal import pause

button = Button(27)
led = LED(17)

def led_on():
    print("LED on")

def led_off():
    print("LED off")

def loop():
    while True:
        # Here we can use the library's methods for the Button object:
        button.when_pressed = led_on
        button.when_released = led_off

        led.source = button # The source attribute of LED class receives te signal from the button to switch between on and off

        pause() # Used to avoid overloading the RPi CPU with continuous data been checked from the button status

def destroy():
    button.close()
    led.close()

if __name__ == '__main__': # Program start from here
    try:
        loop()
    except KeyboardInterrupt: # When 'Ctrl+C' is pressed, the childprogram destroy() will be executed.
        destroy()