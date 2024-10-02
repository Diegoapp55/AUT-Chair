import time
from gpiozero import OutputDevice

SDI = OutputDevice(17)
RCLK = OutputDevice(27)
SRCLK = OutputDevice(22)

#=============== LED Mode Defne ================
# You can define yourself, in binay, and convert it to Hex
# 8 bits a group, 0 means off, 1 means on
# like : 0101 0101, means LED1, 3, 5, 7 are on.(from left to right)
# and convert to 0x55.
MODE0 = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80] #original mode
MODE1 = [0x01,0x03,0x07,0x0f,0x1f,0x3f,0x7f,0xff] #blink mode 1
MODE2 = [0x00,0x81,0xc3,0xe7,0xff,0x7e,0x3c,0x18,0x00] #blink mode 2
MODE3 = [0x00,0x02,0x03,0x0b,0x0f,0x2f,0x3f,0xbf,0xff] #blink mode 3
RESET = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00] #mode when program ends
#=================================================
def print_msg():
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

def hc595_in(dat):
    for bit in range(0, 8):
        if 0x80 & (dat << bit):
            SDI.on()
        else:
            SDI.off()
        SRCLK.on()
        time.sleep(0.001)
        SRCLK.off()

def hc595_out():
    RCLK.on()
    time.sleep(0.001)
    RCLK.off()

def loop():
    WhichLeds = MODE2 # Change Mode, modes from LED0 to LED3
    sleeptime = 0.3 # Change speed, lower value, faster speed
    while True:
        for i in range(0, len(WhichLeds)):
            hc595_in(WhichLeds[i])
            hc595_out()
            time.sleep(sleeptime)
        for i in range(len(WhichLeds)-1, -1, -1):
            hc595_in(WhichLeds[i])
            hc595_out()
            time.sleep(sleeptime)
    

def destroy(): # When program ending, the function is executed.
    for bit in range(0, 8):
        SDI.off()
        SRCLK.on()
        time.sleep(0.001)
        SRCLK.off()
    hc595_out()
    SDI.close()
    RCLK.close()
    SRCLK.close()

if __name__ == '__main__': # Program starting from here
    print_msg()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()