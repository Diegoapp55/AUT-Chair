#!/usr/bin/env python

# Import the necessary libraries
from gpiozero import LED  # Import the LED class from the gpiozero library
import time  # Import the time module for delays

# Define the GPIO pins for the LEDs
pins = [20, 17, 27, 22, 6, 13, 19, 21]  # List of GPIO pin numbers

def loop():
    """Continuously cycle through the LED pins, turning each LED on and off."""
    while True:  # Infinite loop to keep the program running
        # Cycle through the pins in the original order
        for pin in pins:
            led = LED(pin)  # Initialize the LED on the specified GPIO pin
            led.on()  # Turn the LED on (set pin to +3.3V)
            time.sleep(0.2)  # Keep the LED on for 0.2 seconds
            led.off()  # Turn the LED off
            led.close()  # Release the resources associated with the LED

        # Cycle through the pins in reverse order
        for pin in pins[::-1]:  # Reverse the list of pins
            led = LED(pin)  # Initialize the LED on the specified GPIO pin
            led.on()  # Turn the LED on (set pin to +3.3V)
            time.sleep(0.2)  # Keep the LED on for 0.2 seconds
            led.off()  # Turn the LED off
            led.close()  # Release the resources associated with the LED

if __name__ == '__main__':  # Check if the script is being run directly
    try:
        loop()  # Start the loop function to control the LEDs
    except KeyboardInterrupt:  # Handle the interruption (Ctrl+C)
        print("\nProgram ended")  # Print a message when the program is terminated

