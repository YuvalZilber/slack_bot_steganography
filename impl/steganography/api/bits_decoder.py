from __future__ import annotations

from abc import ABC
from typing import Iterable, Generic

from impl.steganography.api.utilities.consts import Bit, ContentType


class BitsDecoder(Generic[ContentType], ABC):
    def write_bit(self, bit):
        raise NotImplementedError()

    def write(self, data, bits_per_write):
        for i in range(bits_per_write):
            self.write_bit((data >> (bits_per_write - i - 1)) % 2)

    def read(self):
        raise NotImplementedError()

    def decode(self, bits: Iterable[Bit]) -> ContentType:
        raise NotImplementedError()
