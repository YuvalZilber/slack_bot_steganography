from __future__ import annotations

from abc import ABC
from typing import Any


class ResponseField(ABC):
    subclasses: dict[str, type[ResponseField]] = {}

    def __init__(self, value: Any):
        self._value = value

    def to_block(self) -> dict[str, Any]:
        raise NotImplementedError()

    def __init_subclass__(cls):
        cls.subclasses[cls.name()] = cls

    def __bool__(self):
        return self._value is not None

    @classmethod
    def name(cls):
        raise NotImplementedError()


class FieldText(ResponseField):
    @classmethod
    def name(cls):
        return "text"

    def to_block(self) -> dict[str, Any]:
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": self._value
            }
        }


class FieldImage(ResponseField):
    @classmethod
    def name(cls):
        return "image"

    def to_block(self) -> dict[str, Any]:
        return {
            "type": "image",
            "image_url": f"{self._value}",
            "alt_text": "images"
        }
