from __future__ import annotations

import itertools
from typing import Iterable

from packs.steganography.api.bits_decoder import BitsDecoder
from packs.steganography.api.bits_encoder import BitsEncoder
from packs.steganography.api.decrypter import StegImageDecrypter
from packs.steganography.api.encrypter import StegImageEncrypter
from packs.steganography.api.encrypter_decrypter import StegImageEncrypterDecrypter
from packs.steganography.api.utilities.consts import Bit, one, zero, Byte, Bytes
from packs.steganography.api.utilities.functions import split_bits


class StegSimpleImageEncrypter(StegImageEncrypter[str]):
    def _get_encoder(self, message: str) -> BitsEncoder:
        return SimpleEncoder(message)

    def _get_settings(self) -> Iterable[Bit]:
        return [one for _ in range(self.bits_per_pixel)] + [zero]


class StegSimpleImageDecrypter(StegImageDecrypter[str]):
    def _get_decoder(self) -> BitsDecoder[str]:
        return SimpleDecoder()

    def _extract_encryption_settings(self) -> int:
        c = 0
        for pixel in self._flat_image:
            if pixel % 2 == zero:
                break
            c += 1
        self._flat_image = self._flat_image[c + 1 :]
        return c


class StegSimpleImageEncrypterDecrypter(StegImageEncrypterDecrypter[str]):
    def _get_suffix(self) -> list[Bit]:
        return [zero] * 8

    def _make_encrypter(self, settings: int) -> StegImageEncrypter:
        return StegSimpleImageEncrypter(self._carrier, self._get_suffix(), settings)

    def _make_decrypter(self) -> StegImageDecrypter:
        return StegSimpleImageDecrypter(self._carrier, self._get_suffix())


class SimpleDecoder(BitsDecoder[str]):
    def read(self):
        return bytes(self.bytes).decode("utf8")

    def __init__(self):
        self.bytes = []
        self.cur_byte = 0
        self.left_bits = 8
        self.stop = False

    def write_bit(self, bit):
        self.cur_byte = (self.cur_byte << 1) + bit
        self.left_bits -= 1
        if self.left_bits == 0:
            appended = self.cur_byte
            self.bytes.append(appended)
            self.cur_byte = 0
            self.left_bits = 8
            return self._decode(appended)

    def write(self, data, bits_per_write):
        ret = None
        bits_to_take = min(bits_per_write, self.left_bits)
        result, curry = split_bits(data, bits_per_write - bits_to_take)
        self.cur_byte = (self.cur_byte << bits_to_take) + result
        if self.left_bits <= bits_per_write:
            ret = self._decode(self.cur_byte)
            self.bytes.append(self.cur_byte)
            self.cur_byte = curry
        self.left_bits = ((self.left_bits - bits_per_write) % 8) or 8
        return ret

    @staticmethod
    def to_byte(bits: Bytes) -> int:
        assert len(bits) == 8, f"expected len(bits)==8, got len(bits)=={len(bits)}"
        byte = 0
        for bit in bits:
            byte <<= 1
            byte += bit
        return byte

    def decode(self, bits: Iterable[Bit]) -> str:
        bits = list(bits)
        return bytes(
            [self.to_byte(bits[i : i + 8]) for i in range(0, len(bits), 8)]
        ).decode("utf8")

    def _decode(self, byte: int):
        return int(byte).to_bytes(1, "big").decode("utf8")


class TrivialEncoder(BitsEncoder[bytes]):
    def _encode(self):
        return self._content


class SimpleEncoder(BitsEncoder[str]):
    def _encode(self) -> Iterable[Bit]:
        for byte in self._content.encode("utf8"):
            yield from self.encode_byte(byte)

    @staticmethod
    def encode_byte(byte: int) -> Iterable[Byte]:
        yield from map(int, bin(byte).split("b")[-1].zfill(8))

    def is_empty(self) -> bool:
        try:
            b = next(self._buffer)
        except StopIteration:
            return True
        self._buffer = itertools.chain([b], self._buffer)
        return False
