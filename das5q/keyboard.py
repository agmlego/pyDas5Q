# -*- coding: utf-8 -*-
# SPDX-License-Identifier: FAFOL

from typing import NamedTuple
import hid

from .packets import PACKET_LENGTH, AckPacket, Packet
import logging

logger = logging.getLogger(__name__)


class KeyboardNotFoundError(Exception):
    pass


class Keyboard:
    _hid_device = None  # instance of pyhidapi
    _vid = 0x24F0
    _pid = 0x2020
    _usage = 165
    _interface_number = 2
    _sequence = 0

    regions = {}

    def __init__(self, path):
        self._hid_path = path

    def __enter__(self):
        '''Connect to the device.'''
        self._hid_device = hid.Device(path=self._hid_path)
        self._hid_device.__enter__()
        return self

    def __exit__(self, *args):
        '''Disconnect from the device.'''
        self._hid_device.__exit__(*args)

    @classmethod
    def search(cls):
        '''Find and return a reference to the das 5Q keyboard.

        Raises:
            KeyboardNotFoundError if no keyboard was found

        '''
        interfaces = hid.enumerate(vid=cls._vid, pid=cls._pid)
        for interface in interfaces:
            if interface['usage'] == cls._usage and interface['interface_number'] == cls._interface_number:
                return cls(path=interface['path'])
        else:
            raise KeyboardNotFoundError(
                f'No device found for {cls._vid}:{cls._pid}')

    def _write(self, data: Packet) -> int:
        '''Write data to the device.

        Returns:
            the sequence number used for the write

        '''
        logger.debug(
            f'Writing packet to keyboard (seq={self._sequence}): {data!r}')
        data = bytes(data)
        # inject sequence number into the fourth byte
        data = data[:3] + bytes([self._sequence]) + data[4:]
        sequence = self._sequence
        self._sequence = (sequence + 1) % 0x100
        self._hid_device.send_feature_report(data)
        return sequence

    def _read(self) -> tuple[Packet, int]:
        '''Read data from device.'''
        response = Packet.parse(
            self._hid_device.get_feature_report(0, PACKET_LENGTH))
        packet, seq = response
        logger.debug(f'Got packet (seq={seq}) from keyboard: {packet!r}')
        return response

    def make_request(self, data: Packet):
        '''Make a request with device.

        Returns:
            None if no Packets
            One Packet if only one received
            List of Packets if more than one received

        '''
        seq = self._write(data)
        response = self._read()
        ack, ack_seq = response
        assert ack_seq == seq
        assert isinstance(ack, AckPacket)
        results = []
        while True:
            packet, seq = self._read()
            if seq == ack_seq:
                break
            else:
                results.append(packet)
        if len(results) == 1:
            results = results[0]
        elif len(results) == 0:
            results = None
        return results

class Rectangle(NamedTuple):
    top:float
    left:float
    width:float
    height:float

class Region:
    leds: list
    description: str
    short_name: str
    rectangle: Rectangle

    def __init__(self,short_name,description,rectangle,leds=None):
        self.short_name = short_name
        self.description = description
        self.rectangle = rectangle
        self.leds = leds
