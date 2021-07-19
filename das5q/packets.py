# -*- coding: utf-8 -*-
# SPDX-License-Identifier: FAFOL

import struct
from typing import Dict, Sequence

PACKET_LENGTH = 65

TYPES = {}


class Packet:
    '''Generic packet.'''

    type = 0x00
    fields = []
    headerformat = '<xxBx'
    format = ''

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            assert name in self.fields
            setattr(self, name, value)

    def __init_subclass__(cls):
        '''Build up a dictionary of packet types'''
        if cls.type not in TYPES:
            TYPES[cls.type] = cls
        else:
            # if there are collisions, use the command value as a subkey
            if not isinstance(TYPES[cls.type], dict):
                other = TYPES[cls.type]
                TYPES[cls.type] = {}
                TYPES[cls.type][other.command] = other

            TYPES[cls.type][cls.command] = cls

    def __bytes__(self):
        message = struct.pack(
            self.headerformat + self.format,
            self.type,
            *[getattr(self, field) for field in self.fields]
        )
        assert len(message) <= PACKET_LENGTH
        return message.ljust(PACKET_LENGTH, b'\x00')

    def __repr__(self):
        return f'<{type(self).__name__} type={self.type:02X}: {" ".join([f"{field}={getattr(self,field)}" for field in self.fields])}>'

    @staticmethod
    def parse(packet_data: bytes) -> 'Packet':
        '''Figure out what type of packet this is, and return an object of that type.'''
        packettype, = struct.unpack(Packet.headerformat, packet_data[:4])
        if isinstance(TYPES[packettype], dict):
            # there are collisions, use the command value as a subkey
            packet = TYPES[packettype][packet_data[len(Packet.headerformat)]]
        else:
            packet = TYPES[packettype]
        fields = struct.unpack(packet.format, packet_data[4:])
        return packet(**dict(zip(packet.fields, fields)))


class InitializePacket(Packet):
    '''Initialize connection with keyboard.'''

    type = 0x13
    fields = ['mystery']
    format = '32s'
    mystery = bytes([
        0x4d, 0x43, 0x49, 0x51, 0x46, 0x49, 0x46, 0x45,
        0x44, 0x4c, 0x48, 0x39, 0x46, 0x34, 0x41, 0x45,
        0x43, 0x58, 0x39, 0x31, 0x36, 0x50, 0x42, 0x44,
        0x35, 0x50, 0x33, 0x41, 0x33, 0x30, 0x37, 0x38
    ])


class FirmwareRequestPacket(Packet):
    '''Request keyboard firmware version.'''

    type = 0x11
    fields = ['mystery']
    format = '32s'
    mystery = bytes([
        0x4d, 0x43, 0x49, 0x51, 0x46, 0x49, 0x46, 0x45,
        0x44, 0x4c, 0x48, 0x39, 0x46, 0x34, 0x41, 0x45,
        0x43, 0x58, 0x39, 0x31, 0x36, 0x50, 0x42, 0x44,
        0x35, 0x50, 0x33, 0x41, 0x33, 0x30, 0x37, 0x38
    ])


class FirmwareVersionPacket(Packet):
    '''Reply containing firmware version.'''

    type = 0x15
    fields = ['major', 'minor', 'patch', 'build']
    format = '4B'
    major = 0
    minor = 0
    patch = 0
    build = 0

    def __str__(self):
        return f'{self.major}.{self.minor}.{self.patch}.{self.build}'


class FreezeEffectsPacket(Packet):
    '''Freeze effects on keyboard.'''

    type = 0x2D
    fields = ['command', 'mystery']
    format = 'B28s'
    command = 0x07
    mystery = bytes([0xFF]*28)


class TriggerPacket(Packet):
    '''Apply all changes to keyboard.'''

    type = 0x2D
    fields = ['command', 'mystery']
    format = 'B28s'
    command = 0x0F
    mystery = bytes([0xFF]*28)


class BrightnessPacket(Packet):
    '''Set overall keyboard brightness.'''

    type = 0x2B
    fields = ['brightness']
    format = 'B'
    brightness = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert 0 <= self.brightness <= 63


class StatePacket(Packet):
    '''Set key state.'''

    type = 0x28
    fields = [
        'color_channel_id',
        'mystery_1'
        'key',
        'effect_id',
        'up_max_level',
        'up_increment',
        'up_increment_delay',
        'up_hold_level',
        'up_hold_delay',
        'down_min_level',
        'down_decrement',
        'down_decrement_delay',
        'down_hold_level',
        'down_hold_delay',
        'start_delay',
        'mystery_2',
        'effect_flag',
    ]
    format = '4B13H'

    color_channel_id = 0
    mystery_1 = 1
    key = 151
    effect_id = 0x02  # TODO: maybe make self an Enum options are 0x00 or 0x02
    up_max_level = 0
    up_increment = 0
    up_increment_delay = 0
    up_hold_level = 0
    up_hold_delay = 0
    down_min_level = 0
    down_decrement = 0
    down_decrement_delay = 0
    down_hold_level = 0
    down_hold_delay = 0
    start_delay = 0
    mystery_2 = 0
    # TODO: effect_flag has no default???

    def __init__(self, *, effect_flag: 'EffectFlag', **kwargs):
        super().__init__(effect_flag=effect_flag, **kwargs)


class AckPacket(Packet):
    type = 0x14
    fields = []


class EffectFlag:
    '''Effect flag definition.'''

    value = 1
    incrementOnly = 0x01
    decrementOnly = 0x02
    incrementDecrement = 0x19
    decrementIncrement = 0x1A
    triggerLaterMask = 0x4000
    transitionMask = 0x1000

    def setIncrementDecrement(self):
        self.value = self.incrementDecrement

    def setDecrementIncrement(self):
        self.value = self.decrementIncrement

    def setIncrementOnly(self):
        self.value = self.incrementOnly

    def setDecrementOnly(self):
        self.value = self.decrementOnly

    def setTriggerEffectOnApply(self):
        self.value = self.value | self.triggerLaterMask

    def setTriggerEffectNow(self):
        self.value = self.value & ~self.triggerLaterMask

    def setEnableTransition(self):
        self.value = self.value & ~self.transitionMask

    def setDisableTransition(self):
        self.value = self.value | self.transitionMask

    def __index__(self):
        return self.value
