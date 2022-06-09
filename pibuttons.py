#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pibuttons.py
#
# Based on https://github.com/stenobot/SoundMatrixPi
#

import RPi.GPIO as GPIO
import time

class ButtonMatrix():

    def __init__(self):
        """Initialize ButtonMatrix internal data and GPIO."""
        GPIO.setmode(GPIO.BCM)

        # matrix button ids
        self.buttonIDs = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
        # gpio inputs for rows - top to bottom
        self.rowPins = [27,22,5,6]
        # gpio outputs for columns - left to right
        self.columnPins = [25, 26, 19, 13, ]
        # buttons held down
        self.buttons = [ [ 0 for c in self.columnPins ] for r in self.rowPins ]
        self.pressed = [ [ 0 for c in self.columnPins ] for r in self.rowPins ]

        # define four inputs with pull up resistor
        for i in range(len(self.rowPins)):
            GPIO.setup(self.rowPins[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

        # define four outputs and set to high
        for j in range(len(self.columnPins)):
            GPIO.setup(self.columnPins[j], GPIO.OUT)
            GPIO.output(self.columnPins[j], 1)
            # Actually, set four columns to tristate input.
            GPIO.setup(self.columnPins[j], GPIO.IN, pull_up_down = GPIO.PUD_OFF)

    def check(self, t=0.1, n=3):
        """Return list of pressed button(s) in button grid with delay of
        t seconds and a debounce for t * n seconds."""
        for i in range(len(self.rowPins)):
            for j in range(len(self.columnPins)):
                # set each column pin to output low
                GPIO.setup(self.columnPins[j], GPIO.OUT)
                GPIO.output(self.columnPins[j], 0)
                # check column for this row
                if GPIO.input(self.rowPins[i]) == 0:
                    # print(f"button {self.buttonIDs[i][j]} pressed")
                    # print(f"{self.buttons}")
                    self.buttons[i][j] = t
                elif self.buttons[i][j] > 0:
                    self.buttons[i][j] += t
                # return each column pin to output high
                # GPIO.output(self.columnPins[j], 1)
                # Reset each column pin to tristate input.
                GPIO.setup(self.columnPins[j], GPIO.IN, pull_up_down = GPIO.PUD_OFF)

        # Sleep for t seconds to allow for debouncing.
        time.sleep(t)

        # Update self.pressed with one-shot debounced button IDs and return list.
        for r in range(len(self.buttons)):
            for c in range(len(self.buttons[r])):
                if self.buttons[r][c] > n * t:
                    self.pressed[r][c] = self.buttonIDs[r][c]
                    self.buttons[r][c] = 0
                else:
                    self.pressed[r][c] = 0
        return [ v for row in self.pressed for v in row if v ]

    def cleanup(self):
        """Cleanup GPIO."""
        GPIO.cleanup()

def main():
    # initial the button matrix
    buttons = ButtonMatrix()
    # Check buttons (up to) m times / second.
    m, n = 50, 0
    try:
        while(True):
            n += 1
            pressed = buttons.check(1 / m)
            # Print results every second or whenever buttons are released.
            if n % m == 0 or pressed:
                print(pressed)
    except KeyboardInterrupt:
        buttons.cleanup()

if __name__ == "__main__":
    main()
