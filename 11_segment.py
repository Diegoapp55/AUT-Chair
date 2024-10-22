import time
from gpiozero import OutputDevice

# Define output pins for the shift register
SDI = OutputDevice(17)  # Serial Data Input
RCLK = OutputDevice(27)  # Register Clock
SRCLK = OutputDevice(22)  # Shift Register Clock

#=============== LED Mode Define ================
# The codes in Hexagesimal form below indicate the segments of
# the display that are turned on. Where the LSB means Segment A
# and the MSB means Decimal Point (DP). For example: 0x4f means
# 0 1 0 0 1 1 1 1, i.e. A, B, C, D and G are on, and number 3 is
# shown on the display.
segCode = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 
           0x7f, 0x6f, 0x77, 0x7c, 0x39, 0x5e, 0x79, 0x71, 0x80]  # Segment patterns
RESET = [0x00] * 16  # Reset state for display
#=================================================

def print_msg():
    # Display startup message
    print('Program is running...')
    print('Please press Ctrl+C to end the program...')

def hc595_op(dat):
    # Send data to the shift register
    for bit in range(0, 8):
        if 0x80 & (dat << bit):
            SDI.on()  # Set SDI high for segment
        else:
            SDI.off()  # Set SDI low
        SRCLK.on()  # Pulse the shift clock
        time.sleep(0.001)  # Short delay
        SRCLK.off()
    RCLK.on()  # Latch the data
    time.sleep(0.001)  # Short delay
    RCLK.off()

def loop():
    # Main loop to display numbers
    WhichLeds = segCode  # Select segment codes
    sleeptime = 0.3  # Delay between updates
    while True:
        for i in range(0, len(WhichLeds)):
            hc595_op(WhichLeds[i])  # Update display
            time.sleep(sleeptime)  # Wait before next update

def destroy():
    # Cleanup function on exit
    for bit in range(0, 8):
        SDI.off()  # Turn off all segments
        SRCLK.on()
        time.sleep(0.001)
        SRCLK.off()
    RCLK.on()  # Latch off state
    time.sleep(0.001)
    RCLK.off()
    SDI.close()  # Close pin resources
    RCLK.close()
    SRCLK.close()

if __name__ == '__main__':  # Start of the program
    print_msg()  # Show messages
    try:
        loop()  # Run the main loop
    except KeyboardInterrupt:
        destroy()  # Cleanup on exit
