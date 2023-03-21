import itertools
from abc import ABC
from typing import Iterable, Optional

import numpy as np

from impl.steganography.api.bits_encoder import BitsEncoder
from impl.steganography.api.common import Steganographer, ImageSteganographer
from impl.steganography.api.utilities.consts import Bit, ContentType, CarrierType, EncSettingsType
from impl.steganography.api.utilities.functions import FlagIterator, const_iterator


class StegEncrypter(Steganographer[CarrierType, ContentType, EncSettingsType], ABC):
    """
    its job is to encrypt the content in to the carrier
    For performance consideration, by convention, it is done in-place
    """

    def __init__(self, carrier: CarrierType, suffix: Iterable[Bit], settings: EncSettingsType):
        super().__init__(carrier, suffix)
        self._settings = settings

    def encrypt(self, content: ContentType) -> CarrierType:
        msg_length = len(content)
        if self._settings is None:
            self._settings = self._best_settings_to_fit_message(msg_length)
        try:
            max_length = self._max_message_size()
        except:
            max_length = -1
        if msg_length > max_length:
            error_message = f"Can't encode content of length {msg_length} to this carrier. \n" \
                            f"The maximum content length for " \
                            f"settings '{self._get_settings()}' in this carrier is {max_length}\n"
            best_settings = self._best_settings_to_fit_message(msg_length)
            if best_settings is not None:
                error_message += f"settings that could fit this content: {best_settings}"
            else:
                error_message += "Even modifying settings won't help you to fit this content."
            raise ValueError(error_message)
        return self._encrypt(content)

    def _encrypt(self, content: ContentType) -> CarrierType:
        """take the content, returns the carrier with the encrypted data in it"""
        raise NotImplementedError()

    def _get_encoder(self, content: ContentType) -> BitsEncoder:
        """Implementation should be 1 line, return an initialized encoder for the data"""
        raise NotImplementedError()

    def _get_settings(self) -> Iterable[Bit]:
        """
        Each encryption should start with a brief encryption settings for the decrypter.
        If your decrypter doesn't need it - return []
        otherwise, you should encrypt those bits into the carrier in a way the decoder could extract it.
        * Remember - the receiver of the message don't know anything about how it was encrypted
        """
        raise NotImplementedError()

    def _max_message_size(self) -> int:
        """
        Each message have a mean to measure size.
        Return the size that beyond it, encryption could not be done, you would need
        either a bigger carrier or more detectable settings
        """
        raise NotImplementedError()

    def _best_settings_to_fit_message(self, message_size: int) -> Optional[EncSettingsType]:
        """
        For a message of this size, return the best (least detectable) settings to encrypt on the given carrier
        return None if you can't (or don't want to) guess suitable setting
        """
        raise NotImplementedError()


class StegImageEncrypter(StegEncrypter[np.ndarray, ContentType, int], ImageSteganographer[ContentType], ABC):
    def _encrypt(self, content: ContentType) -> np.ndarray:
        """take the content, returns the carrier with the encrypted data in it"""
        bpp = self.bits_per_pixel
        settings_bits = self._get_settings()
        image = self._flat_image
        flag = FlagIterator()
        to_encode = itertools.chain(zip(settings_bits, const_iterator(1)),
                                    zip(self._get_encoder_iterator(content), const_iterator(bpp)),
                                    flag,
                                    zip(self._suffix, const_iterator(bpp)))
        try:
            for i, (bits, length) in enumerate(to_encode):
                left_of_pixel = (image[i] >> length) << length
                image[i] = left_of_pixel + bits
        except IndexError:
            if not flag:
                raise
        return self.image

    @property
    def bits_per_pixel(self) -> int:
        return self._settings

    def _get_encoder_iterator(self, content):
        encoder: BitsEncoder = self._get_encoder(content)
        while True:
            try:
                yield encoder.next(self.bits_per_pixel)
            except StopIteration:
                break

    def _get_encoder(self, content: ContentType) -> BitsEncoder:
        """Implementation should be 1 line, return an initialized encoder for the data"""
        raise NotImplementedError()

    def _get_settings(self) -> Iterable[Bit]:
        """
        Each encryption should start with a brief encryption settings for the decrypter.
        If your decrypter doesn't need it - return []
        otherwise, you should encrypt those bits into the carrier in a way the decoder could extract it.
        * Remember - the receiver of the message don't know anything about how it was encrypted
        """
        raise NotImplementedError()

    def _max_message_size(self) -> int:
        """
        as the encoder encode it to bits - the amount of bytes is the length
        """
        bpp = self.bits_per_pixel
        settings_bits = self._get_settings()
        return bpp * (len(self._flat_image) - len(list(settings_bits))) // 8

    def _best_settings_to_fit_message(self, message_size: int) -> Optional[int]:
        """
        For a message of this size, return the best (least detectable) settings to encrypt on the given carrier
        """
        colors = len(self._flat_image)
        delta = colors ** 2 - 2 * colors - 32 * message_size + 1
        if delta < 0:
            return None
        return int(np.ceil((-np.sqrt(delta) + colors - 1) / 2))
