from gpiozero import LED, Button
from signal import pause

button = Button(27)
led = LED(17)

def led_on():
    print("LED on")

def led_off():
    print("LED off")

# Here we can use the library's methods for the Button object:

button.when_pressed = led_on
button.when_released = led_off

led.source = button # The source attribute of LED class receives te signal from the button to switch between on and off

pause() # Used to avoid overloading the RPi CPU with continuous data been checked from the button status