#!/usr/bin/env python

# Import the necessary libraries
from gpiozero import PWMLED  # Import the PWMLED class from the gpiozero library
import time  # Import the time module for delays

# Initialize the PWM LED on GPIO pin 17 with a frequency of 1 kHz
led = PWMLED(17, frequency=1e3)

def loop():
    """Continuously adjust the brightness of the LED in a loop."""
    while True:  # Infinite loop to keep the program running
        # Gradually increase the brightness of the LED
        for dc in range(0, 101, 4):  # Duty cycle ranges from 0 to 100 in steps of 4
            led.value = dc / 100  # Set the brightness (0 to 1)
            time.sleep(0.05)  # Wait for 50 milliseconds
        
        time.sleep(1)  # Pause for 1 second at full brightness

        # Gradually decrease the brightness of the LED
        for dc in range(100, -1, -4):  # Duty cycle ranges from 100 to 0 in steps of -4
            led.value = dc / 100  # Set the brightness (0 to 1)
            time.sleep(0.05)  # Wait for 50 milliseconds
        
        time.sleep(1)  # Pause for 1 second at minimum brightness

if __name__ == '__main__':  # Check if the script is being run directly
    try:
        loop()  # Start the loop function to control the LED brightness
    except KeyboardInterrupt:  # Handle the interruption (Ctrl+C)
        print("\nProgram ended")  # Print a message when the program is terminated
