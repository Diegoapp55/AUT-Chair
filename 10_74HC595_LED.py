import time
from gpiozero import OutputDevice

# Define GPIO pins for controlling the 74HC595 shift register
SDI = OutputDevice(17)   # Serial Data Input
RCLK = OutputDevice(27)  # Register Clock
SRCLK = OutputDevice(22) # Shift Register Clock

def print_msg():
    """Display a message indicating the program is running."""
    print('Program is running...')
    print('Please press Ctrl+C to end the program...')

def hc595_in(dat):
    """Send data to the shift register."""
    for bit in range(0, 8):
        # Check if the current bit should be set (1) or not (0)
        if 0b10000000 & (dat << bit):
            SDI.on()  # Set SDI high
        else:
            SDI.off() # Set SDI low
        
        SRCLK.on()  # Pulse the shift clock
        time.sleep(0.001)  # Small delay
        SRCLK.off() # Stop pulsing

def hc595_out():
    """Latch the data into the output register."""
    RCLK.on()  # Pulse the register clock to latch data
    time.sleep(0.001)  # Small delay
    RCLK.off() # Stop pulsing

def loop(WhichLeds, sleeptime):
    """Main loop to control the LED patterns."""
    while True:
        # Iterate through the selected LED pattern
        for i in range(0, len(WhichLeds)):
            hc595_in(WhichLeds[i])  # Send the current pattern
            hc595_out()              # Latch the data to the outputs
            time.sleep(sleeptime)    # Wait before showing the next pattern
        
        # Reverse the order of the patterns
        for i in range(len(WhichLeds) - 1, -1, -1):
            hc595_in(WhichLeds[i])  # Send the current pattern
            hc595_out()              # Latch the data to the outputs
            time.sleep(sleeptime)    # Wait before showing the next pattern

def destroy(): 
    """Cleanup function executed on program exit."""
    for bit in range(0, 8):
        SDI.off()  # Turn off the data line
        SRCLK.on()  # Pulse the shift clock
        time.sleep(0.001)  # Small delay
        SRCLK.off() # Stop pulsing
    hc595_out()  # Latch the reset state
    SDI.close()  # Cleanup GPIO
    RCLK.close() # Cleanup GPIO
    SRCLK.close() # Cleanup GPIO

if __name__ == '__main__':  # Entry point for the program
    #=============== LED Mode Definitions ================
    # Define various LED patterns in binary
    # Each entry corresponds to 8 bits; 0 means off, 1 means on.
    # For example: 0b01010101 means LED1, 3, 5, 7 are on (from left to right)
    # Note: 0b at the beggining of each number is the notation for a BIN number
    # in Phython.
    MODE0 = [0b00000001,
             0b00000010,
             0b00000100,
             0b00001000,
             0b00010000,
             0b00100000,
             0b01000000,
             0b10000000]  # Original mode
    MODE1 = [0b00000001,
             0b00000011,
             0b00000111,
             0b00001111,
             0b00011111,
             0b00111111,
             0b01111111,
             0b11111111]  # Blink mode 1
    MODE2 = [0b00000000,
             0b10000001,
             0b11000011,
             0b11100111,
             0b11111111,
             0b01111110,
             0b00111100,
             0b00011000,
             0b00000000]  # Blink mode 2
    MODE3 = [0b00000000,
             0b00000010,
             0b00000011,
             0b00001011,
             0b00001111,
             0b00101111,
             0b00111111,
             0b10111111,
             0b11111111]  # Blink mode 3
    RESET = [0b00000000]  # Reset mode when program ends

    #=====================================================

    print_msg()  # Display the initial message

    WhichLeds = MODE2  # Select the LED mode from the list above
    sleeptime = 0.3    # Control the speed of the pattern (lower is faster)

    try:
        loop(WhichLeds, sleeptime)  # Start the main loop
    except KeyboardInterrupt:
        destroy()  # Clean up on exit
