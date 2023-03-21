from abc import ABC

import numpy as np

from impl.steganography.api.bits_decoder import BitsDecoder
from impl.steganography.api.common import Steganographer, ImageSteganographer
from impl.steganography.api.utilities.consts import ContentType, CarrierType, EncSettingsType, Bit
from impl.steganography.api.utilities.limited_buffer import LimitedBuffer


class StegDecrypter(Steganographer[CarrierType, ContentType, EncSettingsType], ABC):
    """
    its job is to encrypt the content in to the carrier
    For performance consideration, by convention, it is done in-place
    """

    def decrypt(self) -> CarrierType:
        """take the content, returns the carrier with the encrypted message in it"""
        raise NotImplementedError()

    def _get_decoder(self) -> BitsDecoder:
        """Implementation should be 1 line, return an initialized decoder for the data"""
        raise NotImplementedError()

    def _extract_encryption_settings(self) -> EncSettingsType:
        """
        Each encryption should start with a brief encryption settings for the decrypter.
        Extract it.
        """
        raise NotImplementedError()


class StegImageDecrypter(StegDecrypter[np.ndarray, ContentType, int], ImageSteganographer[ContentType], ABC):
    def decrypt(self) -> np.ndarray:
        bits_per_pixel = self._extract_encryption_settings()
        decoder: BitsDecoder = self._get_decoder()

        bits = (1 << bits_per_pixel) - 1
        len_suf = len(self._suffix)
        buffer: LimitedBuffer[Bit] = LimitedBuffer(len_suf * 2)
        for pixel in self._flat_image:
            to_decode = pixel & bits
            decoder.write(to_decode, bits_per_pixel)
            buffer.write(*[(to_decode >> i) & 1 for i in range(bits_per_pixel - 1, 0 - 1, -1)])
            if len(buffer) >= len_suf and buffer.pop(len_suf) == self._suffix:
                return decoder.read()[:-len(decoder.decode(self._suffix))]
        return decoder.read()
