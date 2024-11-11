import time
from gpiozero import OutputDevice, Button
import random


# Dictionary to obtain the hexadecimal repression of Decimal numbers
#=============== LED Mode Define ================
# The codes in Hexagesimal form below indicate the segments of
# the display that are turned on. Where the LSB means Segment A
# and the MSB means Decimal Point (DP). For example: 0x4f means
# 0 1 0 0 1 1 1 1, i.e. A, B, C, D and G are on, and number 3 is
# shown on the display.
HexaRepre = {
    #0x3f:0,
    0x06:1,
    0x5b:2, 
    0x4f:3,
    0x66:4,
    0x6d:5,
    0x7d:6
}


# Define output pins for the shift register
SDI = OutputDevice(17)  # Serial Data Input
RCLK = OutputDevice(27)  # Register Clock
SRCLK = OutputDevice(22)  # Shift Register Clock
button = Button(6)
#=============== LED Mode Define ================
# The codes in Hexagesimal form below indicate the segments of
# the display that are turned on. Where the LSB means Segment A
# and the MSB means Decimal Point (DP). For example: 0x4f means
# 0 1 0 0 1 1 1 1, i.e. A, B, C, D and G are on, and number 3 is
# shown on the display.
segCode = list(HexaRepre.keys())  # Segment patterns
ruletcode = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20]  #Rulet pattern
RESET = [0x00] * 16  # Reset state for display

def print_msg():
    # Display startup message
    print('Program is running...')
    print('Please press Ctrl+C to end the program...')

def hc595_op(dat):
    # Send 8 bits to shift register
    for bit in range(0, 8):
        if 0x80 & (dat << bit):
            SDI.on()  # Set SDI high for segment
        else:
            SDI.off()  # Set SDI low
        SRCLK.on()  # Pulse shift clock
        time.sleep(0.001)  # Short delay
        SRCLK.off()
    RCLK.on()  # Latch data into register
    time.sleep(0.001)  # Short delay
    RCLK.off()

def loop(code, type=False):
    # Main loop to display numbers or sequence
    if type:
        number = random.randint(0, 5)  # Random number for display
        print(number+1)
        hc595_op(code[number])  # Display the random number
    else:
        for i in range(len(code)):
            hc595_op(code[i])  # Show sequence on display
            time.sleep(0.1)  # Delay between updates

def destroy():
    # Clean up on exit
    for bit in range(0, 8):
        SDI.off()  # Turn off all segments
        SRCLK.on()
        time.sleep(0.001)
        SRCLK.off()
    RCLK.on()  # Latch off state
    time.sleep(0.001)
    RCLK.off()
    SDI.close()  # Close resources
    RCLK.close()
    SRCLK.close()
    button.close()
    print("Program Ended")

if __name__ == '__main__':  # Start of the program
    print_msg()  # Show startup message
    try:
        while True:
            button.wait_for_press()  # Wait for button press
            loop(ruletcode)  # Show ruleta sequence
            loop(segCode, True)  # Show random number

    except KeyboardInterrupt:
        destroy()  # Cleanup on exit
