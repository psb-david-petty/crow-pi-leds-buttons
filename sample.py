#!/usr/bin/env python3
#
# sample.py
#

import pileds, pibuttons
import time

grid = pileds.PiLEDs()
buttons = pibuttons.ButtonMatrix()

def main():
    while True:
        for i in range(64):
            grid.clear()
            grid.set(i // 8, i % 8, 1)
            pressed = buttons.check()
            if pressed: print(pressed)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        grid.clear()
        buttons.cleanup()
        print('done...')
