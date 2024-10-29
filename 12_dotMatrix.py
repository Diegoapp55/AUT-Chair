import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, CP437_FONT

def output(n, block_orientation, rotate, inreverse, flag):
    # Create a serial interface for the LED matrix
    serial = spi(port=0, device=0, gpio=noop())
    # Initialize the LED matrix device
    device = max7219(serial)

    while flag:
        # Prompt user for text input
        text = input("Write your text: ")
        # Display the input text on the LED matrix
        show_message(device, text, fill="white", font=proportional(CP437_FONT), scroll_delay=0.08)
        # Wait for 1 second before allowing new input
        time.sleep(1)
        # Exit loop if flag is set to False (though it won't happen here)
        if flag == False:
            break
    # The line below is commented out, but could print the last text displayed
    # print(text)

def print_msg():
    # Display a startup message indicating the program is running
    print('Program is running...')
    print('Please press Ctrl+C to end the program...')

if __name__ == "__main__":
    # Set up argument parsing for command line options
    parser = argparse.ArgumentParser(description='view_message arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Argument for number of cascaded LED matrices
    parser.add_argument('--cascaded', '-n', type=int, default=2, help='Number of cascaded MAX7219 LED matrices')
    # Argument for adjusting block orientation
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    # Argument for rotating the display
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
    # Argument for setting reverse order of blocks
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')
    # Uncomment to allow setting a default text message via command line
    # parser.add_argument('--text', '-t', default='>>> No text set', help='Set text message')
    
    # Parse command line arguments
    args = parser.parse_args()
    # Print the startup message
    print_msg()

    try:
        # Call output function with parsed arguments to start displaying messages
        output(args.cascaded, args.block_orientation, args.rotate, args.reverse_order, True)
    except KeyboardInterrupt:
        # Handle the Ctrl+C interruption to end the program gracefully
        output(args.cascaded, args.block_orientation, args.rotate, args.reverse_order, False)
        print("\nProgram ended")
        pass
