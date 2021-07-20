# -*- coding: utf-8 -*-
# SPDX-License-Identifier: FAFOL

from struct import pack
from . import keyboard
from . import packets
from .color import Color


class Das5Q:
    def __init__(self):
        self._keyboard = keyboard.Keyboard.search()

    def __enter__(self):
        '''Connect to the keyboard.'''
        self._keyboard.__enter__()
        self._keyboard.make_request(packets.InitializePacket())
        return self

    def __exit__(self, *args):
        '''Disconnect from the keyboard.'''
        self._keyboard.__exit__(*args)

    def get_firmware_version(self) -> str:
        '''Queries firmware version from keyboard.'''
        return str(self._keyboard.make_request(packets.FirmwareRequestPacket()))

    def write_led_color(self, led: int, color: Color):
        '''Set the chosen LED to the color.

        Keyword Arguments:
            led -- LED index to write
            color -- Color to write to LED

        '''

        effect_flag = packets.EffectFlag()
        effect_flag.setTriggerEffectNow()
        effect_flag.setIncrementOnly()
        for idx, channel in enumerate(color.for_led(led)):
            self._keyboard.make_request(
                packets.StatePacket(
                    key=led,
                    color_channel_id=idx,
                    effect_flag=effect_flag,
                    up_hold_level=channel,
                    up_increment=1,
                    up_increment_delay=5,
                    down_decrement=1,
                    down_decrement_delay=5,

                )
            )

        self._keyboard.make_request(packets.TriggerPacket())
