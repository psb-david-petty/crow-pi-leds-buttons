#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pileds.py
#

"""
pileds.py collects some functions used to drive the 8x8 max7219 LED grid in the PiLEDscass.
"""

__author__ = "David C. Petty"
__copyright__ = "Copyright 2022, David C. Petty"
__license__ = "https://creativecommons.org/licenses/by-nc-sa/4.0/"
__version__ = "0.0.1"
__maintainer__ = "David C. Petty"
__email__ = "david_petty@psbma.org"
__status__ = "Hack"

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas


class PiLEDs:
    """Class to manage the 8x8 max7219 LED grid."""
    _w1, _h1 = 8, 8                         # default width and height

    def __init__(self, lights=[[]], w=_w1, h=_h1,
        block_orientation=0, rotate=0, reverse_order=False):
        """Initialize lights, w, and h and set up serial max7219 device."""
        self._lights = lights
        self._w = w
        self._h = h
        self._serial = spi(port=0, device=1, gpio=noop())
        self._device = \
            max7219(self._serial, width=w, height=h, 
                rotate=rotate, 
                block_orientation=block_orientation,
                blocks_arranged_in_reverse_order=reverse_order)

    @staticmethod
    def _microbitsplit(string):
        """Transform lights string in micro:bit format to a 2D list of digits."""
        return [ [ int(c) for c in row ] for row in string.split(':') ]

    @staticmethod
    def _padleds(lights, w, h):
        """Transform lights 2D list of digits to h x w 2D list of digits."""
        return ([ (row + [ 0, ] * w)[: w]
            for row in lights ] + [ [ 0, ] * w ] * h)[ : h]

    def clear(self):
        """Clear LED grid."""
        self.leds([[]])

    def set(self, r, c, v):
        """Set self._lights[r][c] to v and update LED grid."""
        self._lights[r][c] = v
        self.leds(self._lights)

    def leds(self, lights):
        """Set self._lights to padded lights grid and update LED grid."""
        self._lights = self._padleds(lights, self._w, self._h)
        with canvas(self._device) as draw:
            for r in range(self._h):
                for c in range(self._w):
                    if self._lights[r][c]:
                        # The max7219 is oriented so that (0, 0) is upper left.
                        box = (r, self._w - c - 1, r, self._w - c - 1, )
                        draw.rectangle(box, outline="white")

    def microbitleds(self, string):
        """"Display string in micro:bit format to max7219 LED grid."""
        self.leds(self._microbitsplit(string))


if __name__ == "__main__":
    import time
    smiley = (
        f"00111100:"
        f"01000010:"
        f"10000001:"
        f"10100101:"
        f"10000001:"
        f"10111101:"
        f"01000010:"
        f"00111100:"
    )
    grid = PiLEDs()
    # Test functions on PiLEDs class.
    while True:
        grid.microbitleds(smiley)
        for r in range(PiLEDs._h1):
            for c in range(PiLEDs._w1):
                grid.set(r, c, 1)
                time.sleep(0.1)
        grid.clear()
