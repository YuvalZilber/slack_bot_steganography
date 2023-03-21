from abc import ABC
from typing import Generic, Iterable

import numpy as np

from packs.steganography.api.utilities.consts import (
    Bit,
    ContentType,
    CarrierType,
    EncSettingsType,
    Bytes,
)


class Steganographer(ABC, Generic[CarrierType, ContentType, EncSettingsType]):
    """
    Steganographer is either encrypter or decrypter
    The carrier is the cover media (image, audio, text, etc...)
    The content is the undercover data that is really transmitted
    The settings define a tuning of how the conted is encrypted inside the carrier and the settings too encrypted in
    """

    def __init__(self, carrier: CarrierType, suffix: Iterable[Bit]):
        self._suffix = list(suffix)
        self._carrier: CarrierType = carrier


class ImageSteganographer(Steganographer[np.ndarray, ContentType, int]):
    def __init__(self, carrier: np.ndarray, suffix: Bytes):
        super().__init__(carrier, suffix)
        self._flat_image = self._carrier.reshape(np.prod(self._carrier.shape))

    @property
    def image(self) -> np.ndarray:
        return self._carrier
