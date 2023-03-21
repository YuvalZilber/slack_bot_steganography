from collections import namedtuple
from typing import Any

from slacker.backend.response_fields import ResponseField


def get_name(field_class: type[ResponseField]):
    return field_class.name()


field_classes = ResponseField.subclasses
field_names = field_classes.keys()
Response = namedtuple("Response", field_names=field_names, defaults=[None] * len(field_classes))  # type: ignore


def make_response(**kwargs) -> Response:
    for key, value in kwargs.items():
        kwargs[key] = ResponseField.subclasses[key](value)
    return Response(**kwargs)


def to_message(response: Response) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []

    field: ResponseField
    for field in response:
        if field:
            blocks.append(field.to_block())
    return blocks
