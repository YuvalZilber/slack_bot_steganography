from abc import ABC

import numpy as np

from impl.steganography.api.common import Steganographer
from impl.steganography.api.decrypter import StegImageDecrypter, StegDecrypter
from impl.steganography.api.encrypter import StegImageEncrypter, StegEncrypter
from impl.steganography.api.utilities.consts import CarrierType, ContentType, EncSettingsType, Bit


class StegEncrypterDecrypter(Steganographer[CarrierType, ContentType, EncSettingsType], ABC):
    def __init__(self, carrier: CarrierType):
        super().__init__(carrier, self._get_suffix())

    def encrypt(self, content: ContentType, settings: EncSettingsType) -> CarrierType:
        """take the content, returns the carrier with the encrypted data in it"""
        encrypter: StegEncrypter = self._make_encrypter(settings)
        return encrypter.encrypt(content)

    def decrypt(self) -> CarrierType:
        decrypter: StegDecrypter = self._make_decrypter()
        return decrypter.decrypt()

    def _get_suffix(self) -> list[Bit]:
        raise NotImplementedError()

    def _make_encrypter(self, settings: EncSettingsType) -> StegEncrypter:
        raise NotImplementedError()

    def _make_decrypter(self) -> StegDecrypter:
        raise NotImplementedError()


class StegImageEncrypterDecrypter(StegEncrypterDecrypter[np.ndarray, ContentType, int], ABC):
    def _make_encrypter(self, settings: int) -> StegImageEncrypter:
        raise NotImplementedError()

    def _make_decrypter(self) -> StegImageDecrypter:
        raise NotImplementedError()
