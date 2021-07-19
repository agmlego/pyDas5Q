import struct


class Packet:
    '''Generic packet.'''

    type = 0x00
    fields = []
    headerformat = '<xxcx'
    format = ''

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            assert name in self.fields
            setattr(self, name, value)

    def __bytes__(self):
        return struct.pack(
            self.headerformat + self.format,
            self.type,
            *[getattr(self, field) for field in self.fields]
        )

    def __repr__(self):
        return f'<{type(self).__name__} type={self.type:02X} {" ".join([f"{field}={getattr(self,field)}" for field in self.fields])}>'


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


class FirmwareVersionPacket(Packet):
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


class FreezeEffectsPacket(Packet):
    '''Freeze effects on keyboard.'''

    type = 0x2D
    fields = ['command', 'mystery']
    format = 'c28s'
    command = 0x07
    mystery = bytes([0xFF]*28)


class TriggerPacket(Packet):
    '''Apply all changes to keyboard.'''

    type = 0x2D
    fields = ['command', 'mystery']
    format = 'c28s'
    command = 0x0F
    mystery = bytes([0xFF]*28)


class BrightnessPacket(Packet):
    '''Set overall keyboard brightness.'''

    type = 0x2B
    fields = ['brightness']
    format = 'c'
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
    format = '4c13H'

    color_channel_id = 0
    mystery_1 = 1
    key = 151
    effect_id = 0x02  # TODO: maybe make this an Enum; options are 0x00 or 0x02
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
