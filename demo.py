#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# demo.py
#
# Based on matrix_demo Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT

from pileds import PiLEDs

def demo(w, h, block_orientation, rotate, reverse_order):
    # create matrix device
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, width=w, height=h, rotate=rotate,
        block_orientation=block_orientation, blocks_arranged_in_reverse_order=reverse_order)
    print("Created device")

    # Use PiLEDs, not device created above.
    grid, microbit = PiLEDs(), ''
    for r in range(h):
        for c in range(w):
            microbit += '1'
            PiLEDs().microbitleds(microbit)
            time.sleep(.1)
        microbit += ':'
    grid.clear()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='petty.py arguments, based on matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--width', type=int, default=8, help='Width')
    parser.add_argument('--height', type=int, default=8, help='height')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotation factor')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')

    args = parser.parse_args()

    try:
        demo(args.width, args.height, args.block_orientation, args.rotate, args.reverse_order)
    except KeyboardInterrupt:
        pass
