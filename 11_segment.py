import time
from gpiozero import OutputDevice

SDI = OutputDevice(17)
RCLK = OutputDevice(27)
SRCLK = OutputDevice(22)

#=============== LED Mode Defne ================
# The codes in Hexagesimal form below indicate the segments of
# the display that are turned on. Where the LSB means Segment A
# and the MSB means Decimal Point (DP). For example: 0x4f means
# 0 1 0 0 1 1 1 1, i.e. A, B, C, D and G are on, and number 3 is
# shown on the display.
segCode = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,
           0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71,0x80] #original mode
RESET = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
         ,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00] #mode when program ends
#=================================================
def print_msg():
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

def hc595_op(dat):
    for bit in range(0, 8):
        if 0x80 & (dat << bit):
            SDI.on()
        else:
            SDI.off()
        SRCLK.on()
        time.sleep(0.001)
        SRCLK.off()
    RCLK.on()
    time.sleep(0.001)
    RCLK.off()

def loop():
    WhichLeds = segCode # Change Mode, modes from LED0 to LED3
    sleeptime = 0.3 # Change speed, lower value, faster speed
    while True:
        for i in range(0, len(WhichLeds)):
            hc595_op(WhichLeds[i])
            time.sleep(sleeptime)

def destroy(): # When program ending, the function is executed.
    for bit in range(0, 8):
        SDI.off()
        SRCLK.on()
        time.sleep(0.001)
        SRCLK.off()
    RCLK.on()
    time.sleep(0.001)
    RCLK.off()
    SDI.close()
    RCLK.close()
    SRCLK.close()

if __name__ == '__main__': # Program starting from here
    print_msg()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()