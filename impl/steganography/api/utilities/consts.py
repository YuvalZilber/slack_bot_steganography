from __future__ import annotations

from typing import Literal, TypeVar, Sized

import numpy as np

Bit = Literal[0, 1]
one: Bit = 1
zero: Bit = 0
Bits = TypeVar("Bits", bound=int)
Byte = TypeVar("Byte", bound=np.uint8)
Bytes = TypeVar("Bytes", bound=list[Bit], contravariant=True)
Pixel = TypeVar("Pixel", bound=np.uint8)
ContentType = TypeVar("ContentType", bound=Sized)
CarrierType = TypeVar("CarrierType")
EncSettingsType = TypeVar("EncSettingsType")
