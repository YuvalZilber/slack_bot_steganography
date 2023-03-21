from __future__ import annotations

from abc import ABC
from typing import Generic

from packs.steganography.api.utilities.consts import ContentType


class BitsEncoder(Generic[ContentType], ABC):
    def __init__(self, content: ContentType):
        self._content = content
        self._buffer = iter(self._encode())
        self._stop = False

    def _encode(self):
        raise NotImplementedError()

    def next(self, limit: int) -> int:
        if self._stop:
            raise StopIteration()
        bits = 0
        for i in range(limit):
            try:
                bit = next(self._buffer)
                bits <<= 1
                bits += bit
            except StopIteration:
                if i == 0:
                    raise
                else:
                    bits <<= limit - i
                    self._stop = True
                    break
        return bits
