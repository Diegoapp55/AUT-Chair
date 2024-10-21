#!/usr/bin/env python
# Specify the Python interpreter.

from gpiozero import DigitalInputDevice
# Import DigitalInputDevice for IR receiver.

from signal import pause
# Import pause to wait indefinitely.

IrPin = 6
# Set GPIO pin number for IR receiver.

count = 0
# Initialize signal count.

IRrec = DigitalInputDevice(IrPin, pull_up=True)
# Create an IR receiver instance with pull-up resistor.

def cont():
    # Function to handle received signals.
    
    global count
    # Use global count variable.

    count += 1
    # Increment count.

    print("Received infrared. cnt=", count)
    # Print the count of received signals.

if __name__ == '__main__':  # Start of the program.
    try:
        # Try block for exception handling.

        IRrec.when_deactivated = cont
        # Set event to call cont on signal detection.

        pause()
        # Wait indefinitely for signals.

    except KeyboardInterrupt:  # Handle Ctrl+C interrupt.
        print("\n Program ended")
        # Print end message.

        IRrec.close()
        # Close the IR receiver.
