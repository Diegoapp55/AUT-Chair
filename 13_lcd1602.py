#!/usr/bin/env python
#
# based on code from lrvick and LiquidCrystal
# lrvic - https://github.com/lrvick/raspi-hd44780/blob/master/hd44780.py
# LiquidCrystal - https://github.com/arduino/Arduino/blob/master/libraries/LiquidCrystal/LiquidCrystal.cpp
#
from time import sleep
from gpiozero import DigitalOutputDevice

class Adafruit_CharLCD:
    # commands
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80
    # flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00
    # flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00
    # flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00
    # flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    def __init__(self, pin_rs=17, pin_e=27, pins_db=[5, 6, 13, 19], GPIO =
                None):
        self.pin_rs = DigitalOutputDevice(pin_rs)
        self.pin_e = DigitalOutputDevice(pin_e)
        self.pins_db = [DigitalOutputDevice(pin) for pin in pins_db] # Creates a DigitalOutputDevice object for every pin number of the digital outputs
        self.write4bits(0x33) # initialization
        self.write4bits(0x32) # initialization
        self.write4bits(0x28) # 2 line 5x7 matrix
        self.write4bits(0x0C) # turn cursor off 0x0E to enable cursor
        self.write4bits(0x06) # shift cursor right
        # The | operator mix the binary options to create the Instruction codes for the modes of operation 
        self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF #0000 0100
        self.displayfunction = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5x8DOTS # 0000 0000
        self.displayfunction |= self.LCD_2LINE # 0000 1000
        """ Initialize to default text direction (for romance languages) """
        self.displaymode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode) # set the entry mode
        self.clear()

    def begin(self, cols, lines):
        if (lines > 1):
            self.numlines = lines
            self.displayfunction |= self.LCD_2LINE
            self.currline = 0

    def home(self):
        self.write4bits(self.LCD_RETURNHOME) # set cursor position to zero
        self.delayMicroseconds(3000) # this command takes a long time!

    def clear(self):
        self.write4bits(self.LCD_CLEARDISPLAY) # command to clear display
        self.delayMicroseconds(3000) # 3000 microsecond sleep, clearing the display takes a long time

    def setCursor(self, col, row):
        self.row_offsets = [ 0x00, 0x40, 0x14, 0x54 ]
        if ( row >= self.numlines ):
            row = self.numlines - 1 # we count rows starting w/0
        self.write4bits(self.LCD_SETDDRAMADDR | (col + self.row_offsets[row]))

    def noDisplay(self):
        """ Turn the display off (quickly) """
        self.displaycontrol &= ~self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def display(self):
        """ Turn the display on (quickly) """
        self.displaycontrol |= self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def noCursor(self):
        """ Turns the underline cursor on/off """
        self.displaycontrol &= ~self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursor(self):
        """ Cursor On """
        self.displaycontrol |= self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def noBlink(self):
        """ Turn on and off the blinking cursor """
        self.displaycontrol &= ~self.LCD_BLINKON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def DisplayLeft(self):
        """ These commands scroll the display without changing the RAM """
        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)

    def scrollDisplayRight(self):
        """ These commands scroll the display without changing the RAM """
        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT)

    def leftToRight(self):
        """ This is for text that flows Left to Right """
        self.displaymode |= self.LCD_ENTRYLEFT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

    def rightToLeft(self):
        """ This is for text that flows Right to Left """
        self.displaymode &= ~self.LCD_ENTRYLEFT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

    def autoscroll(self):
        """ This will 'right justify' text from the cursor """
        self.displaymode |= self.LCD_ENTRYSHIFTINCREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

    def noAutoscroll(self):
        """ This will 'left justify' text from the cursor """
        self.displaymode &= ~self.LCD_ENTRYSHIFTINCREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

    def write4bits(self, bits, char_mode=False):
        """ Send command to LCD """
        self.delayMicroseconds(1000) # 1000 microsecond sleep
        bits = bin(bits)[2:].zfill(8) 
        self.pin_rs.value = char_mode # value is a property of DigitalOutputDevice from gpiozero to change either show the logical value of the GPIO pin
        for pin in self.pins_db:
                pin.off()
        for i in range(4):
            if bits[i] == "1":
                self.pins_db[::-1][i].on()
        self.pulseEnable()
        for pin in self.pins_db:
            pin.off()
        for i in range(4,8):
            if bits[i] == "1":
                self.pins_db[::-1][i-4].on()
        self.pulseEnable()

    def delayMicroseconds(self, microseconds):
        seconds = microseconds / float(1000000) # divide microseconds by 1 million for seconds
        sleep(seconds)

    def pulseEnable(self):
        self.pin_e.off()
        self.delayMicroseconds(1) # 1 microsecond pause - enable pulse must be > 450ns
        self.pin_e.on()
        self.delayMicroseconds(1) # 1 microsecond pause - enable pulse must be > 450ns
        self.pin_e.off()
        self.delayMicroseconds(1) # commands need > 37us to settle

    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""
        for char in text:
            if char == '\n':
                self.write4bits(0xC0) # next line
            else:
                self.write4bits(ord(char),True)

def loop():
    lcd = Adafruit_CharLCD()
    # lcd.begin(16, 2)
    while True:
        lcd.clear()
        lcd.message(" LCD 1602 Test \n123456789ABCDEF")
        sleep(2)
        lcd.clear()
        lcd.message("   AUT Chair\n      RUB")
        sleep(2)

if __name__ == '__main__':
    loop()