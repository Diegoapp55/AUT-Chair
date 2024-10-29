import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, CP437_FONT


def output(n, block_orientation, rotate, inreverse,flag):
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    # device = max7219(serial, cascaded, block_orientation=block_orientation,
    #                  rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)
    device = max7219(serial)
    
    while flag:
        text=input("Write your text:" )
        show_message(device, text, fill="white", font=proportional(CP437_FONT), scroll_delay=0.04)
        time.sleep(1)
        if flag == False:
            break
    # print(text)

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='view_message arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=2, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')
    # parser.add_argument('--text', '-t', default='>>> No text set', help='Set text message')
    args = parser.parse_args()

    try:
        output(args.cascaded, args.block_orientation, args.rotate, args.reverse_order, True)
        # output(args.cascaded, args.block_orientation, args.rotate, args.reverse_order, args.text)
    except KeyboardInterrupt:
        output(args.cascaded, args.block_orientation, args.rotate, args.reverse_order, False)
        print("\nProgram ended")
        pass