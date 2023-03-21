from __future__ import annotations

from typing import Iterable

from impl.steganography.api.bits_decoder import BitsDecoder
from impl.steganography.api.bits_encoder import BitsEncoder
from impl.steganography.api.decrypter import StegImageDecrypter
from impl.steganography.api.encrypter import StegImageEncrypter
from impl.steganography.api.encrypter_decrypter import StegImageEncrypterDecrypter
from impl.steganography.api.utilities.consts import Bit, zero
from impl.steganography.samples.simple import SimpleEncoder, SimpleDecoder


class StegBetterSimpleImageEncrypter(StegImageEncrypter[str]):
    def _get_encoder(self, message: str) -> BitsEncoder:
        return SimpleEncoder(message)

    def _get_settings(self) -> Iterable[Bit]:
        return map(int, bin(self._settings - 1).replace("0b", "")[-3:].zfill(3))  # type: ignore


class StegBetterSimpleImageDecrypter(StegImageDecrypter[str]):
    def _get_decoder(self) -> BitsDecoder:
        return SimpleDecoder()

    def _extract_encryption_settings(self) -> int:
        bits = [p % 2 for p in self._flat_image[:3]]
        self._flat_image = self._flat_image[3:]
        return int("".join(map(str, bits)), 2) + 1


class StegBetterSimpleImageEncrypterDecrypter(StegImageEncrypterDecrypter[str]):
    def _get_suffix(self) -> list[Bit]:
        return [zero] * 8

    def _make_encrypter(self, settings: int) -> StegImageEncrypter:
        return StegBetterSimpleImageEncrypter(self._carrier, self._get_suffix(), settings)

    def _make_decrypter(self) -> StegImageDecrypter:
        return StegBetterSimpleImageDecrypter(self._carrier, self._get_suffix())
