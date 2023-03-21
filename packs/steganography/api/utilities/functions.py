from __future__ import annotations

from typing import Any, Iterator, Iterable

from packs.steganography.api.bits_encoder import BitsEncoder

_bit_zerofier = (1 << 8) - 2  # = 1111 1110


def split_bits(bits: int, right_bits_amount: int):
    right = bits & ((1 << right_bits_amount) - 1)
    left = bits >> right_bits_amount
    return left, right


def zerofy_lsb(byte: int) -> int:
    return byte & _bit_zerofier


def encoder_to_iterator(encoder: BitsEncoder, epoch):
    while True:
        yield encoder.next(epoch)


def const_iterator(value: Any):
    while True:
        yield value


class FlagIterator(Iterator, Iterable):
    def __init__(self):
        self._passed_through = False

    def __next__(self):
        self._passed_through = True
        raise StopIteration()

    def __bool__(self):
        return self._passed_through

    def reset(self):
        self._passed_through = False
