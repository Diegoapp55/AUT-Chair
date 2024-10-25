import time
from gpiozero import OutputDevice

# Define GPIO pins for controlling the 74HC595 shift register
SDI = OutputDevice(17)   # Serial Data Input
RCLK = OutputDevice(27)  # Register Clock
SRCLK = OutputDevice(22) # Shift Register Clock

#=============== LED Mode Definitions ================
# Define various LED patterns in binary, converted to hexadecimal
# Each entry corresponds to 8 bits; 0 means off, 1 means on.
# For example: 0101 0101 means LED1, 3, 5, 7 are on (from left to right)
MODE0 = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80] # Original mode
MODE1 = [0x01, 0x03, 0x07, 0x0f, 0x1f, 0x3f, 0x7f, 0xff] # Blink mode 1
MODE2 = [0x00, 0x81, 0xc3, 0xe7, 0xff, 0x7e, 0x3c, 0x18, 0x00] # Blink mode 2
MODE3 = [0x00, 0x02, 0x03, 0x0b, 0x0f, 0x2f, 0x3f, 0xbf, 0xff] # Blink mode 3
RESET = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] # Reset mode when program ends
#=====================================================

def print_msg():
    """Display a message indicating the program is running."""
    print('Program is running...')
    print('Please press Ctrl+C to end the program...')

def hc595_in(dat):
    """Send data to the shift register."""
    for bit in range(0, 8):
        # Check if the current bit should be set (1) or not (0)
        if 0x80 & (dat << bit):
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

def loop():
    """Main loop to control the LED patterns."""
    WhichLeds = MODE2  # Select the LED mode (can change to MODE0, MODE1, or MODE3)
    sleeptime = 0.3    # Control the speed of the pattern (lower is faster)
    
    while True:  # Infinite loop
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
    print_msg()  # Display the initial message
    try:
        loop()  # Start the main loop
    except KeyboardInterrupt:
        destroy()  # Clean up on exit
