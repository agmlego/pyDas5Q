# -*- coding: utf-8 -*-
# SPDX-License-Identifier: FAFOL

from struct import pack
from . import keyboard
from . import packets


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

