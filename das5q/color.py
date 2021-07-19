# -*- coding: utf-8 -*-
# SPDX-License-Identifier: FAFOL

class Color:
    red: int
    green: int
    blue: int

    def __init__(self, red, green=None, blue=None):
        '''Create a new Color.

        Arguments:
            Color('#FFFFFF') # create from RGB hex string
            Color(0xFFFFFF) # create from packed RGB integer
            Color(red=0xFF, green=0xFF, blue=0xFF) # create from channel integers
        '''
        if isinstance(red, str):
            hex = red
            red = int(hex[1:3], 16)
            green = int(hex[3:5], 16)
            blue = int(hex[5:7], 16)

        elif green is None or blue is None:
            pack = red
            red = (pack >> 16) & 0xFF
            green = (pack >> 8) & 0xFF
            blue = pack & 0xFF

        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self) -> str:
        return f'#{self.red:02X}{self.green:02X}{self.blue:02X}'

    def __repr__(self) -> str:
        return f'<Color red={self.red} green={self.green} blue={self.blue}>'

    def __int__(self) -> int:
        '''Return the value as a packed 24-bit integer.'''
        return self.red << 16 | self.green << 8 | self.blue

    def __iter__(self):
        yield self.red
        yield self.green
        yield self.blue

    def for_led(self, index) -> tuple:
        '''Return the values in LED-specific channel ordering

        Keyword Arguments:
            index =-- numeric index of the LED in question

        '''
        # FIXME: Maybe actually do what the docstring says....
        return (self.red, self.green, self.blue)
