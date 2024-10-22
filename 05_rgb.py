from gpiozero import RGBLED # Imports the dedicated class RGBLED from the library, to use its methods
from colorzero import Color # Required to use the color property of RGBLED objects
import time

# Initialize an RGB LED with pins connected to GPIO 17 (red), 27 (green), and 22 (blue)
led = RGBLED(red=17, green=27, blue=22) 
colors = []  # Create a list to store 6 color inputs

# Function to process and validate the RGB input from the user
def process_input(RGB):
    RGB = RGB.strip()  # Remove any leading or trailing whitespace
    splited = RGB.split(',')  # Split the input by commas
    IsValid = True
    
    try:
        # Convert each value (R, G, B) to integers and check for any conversion errors
        R = int(splited[0].strip())  
        G = int(splited[1].strip())  
        B = int(splited[2].strip())
    except (ValueError, IndexError):
        # If there's an error in the input format, raise a ValueError with a clear message
        print("--> Invalid input. Please make sure your input is in the R,G,B form.")
        IsValid = False
        return None, None, None, IsValid  # Return None for R, G, B if the input is invalid
    return R, G, B, IsValid
    
# Function to convert RGB values (0-255) to a range between 0 and 1 for the LED
def RGB(R, G, B):
    R_out = R / 255  # Scale the red value
    G_out = G / 255  # Scale the green value
    B_out = B / 255  # Scale the blue value
    return (R_out, G_out, B_out)

# Main loop to collect RGB inputs and cycle through the colors
def loop():
    # Collect 6 RGB color codes from the user
    for i in range(6):
        while True:
            RGB_usr = input(f'Insert {i+1} RGB color code (in the R,G,B form):')
            R, G, B, IsValid = process_input(RGB_usr)  # Process the input
            if IsValid:
                colors.append([R, G, B])  # Store the color in the list
                break
    
    # Continuously cycle through the input colors
    while True:
        for j in colors:
            # Set the LED to the next color
            led.color = RGB(j[0], j[1], j[2])
            time.sleep(1)  # Wait for 1 second before switching to the next color

# Program entry point
if __name__ == '__main__':
    try:
        loop()  # Run the main loop
    except KeyboardInterrupt:  # Handle 'Ctrl+C' to gracefully exit
        print("\nEnded")
        led.close()  # Release the GPIO pins to avoid errors
