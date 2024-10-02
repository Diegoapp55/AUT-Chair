from gpiozero import RGBLED
from colorzero import Color
import time

led = RGBLED(red=17,green=27,blue=22) 
colors = [] # Create dict for the 6 colors

def process_input(RGB): # Separates R, G and B, checking if sth is wrong on the input
    RGB = RGB.strip()  # Eliminate blank spaces
    splited = RGB.split(',')   # Divide per colon
    try:
        R = int(splited[0].strip())  # Converts to int every code and checks for errors
        G = int(splited[1].strip())  
        B = int(splited[2].strip())
        return R, G, B
    except (ValueError, IndexError):
        raise ValueError("Invalid input. Please make sure your input is in R,G,B form.")
    
def RGB(R,G,B):
    R_out=R/255
    G_out=G/255
    B_out=B/255 
    RGB_out=(R_out,G_out,B_out)
    return RGB_out

def loop():
    for i in range(6):
        RGB_usr = input(f'Insert {i+1} RGB color code (in R,G,B form):')
        R, G, B = process_input(RGB_usr)
        colors.append([R, G, B])
    while True:
        for j in colors:
            led.color = RGB(j[0], j[1], j[2])
            time.sleep(1)

if __name__ == '__main__': # Program start from here
    try:
        loop()
    except KeyboardInterrupt: # When 'Ctrl+C' is pressed, the GPIO pins are released to prevent bugs.
        print("\nEnded")
        led.close()
