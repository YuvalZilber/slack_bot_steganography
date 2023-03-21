import re

import cv2  # type: ignore

from packs.aws import upload
from packs.steganography import StegSimpleImageEncrypterDecrypter as EncrypterDecrypter
from utils import get_image_from_files
from packs.slacker import Response, make_response, bot_command


def encode_and_move(event_ts, image, message, bits_per_pixel=None) -> Response:
    encrypter_decrypter = EncrypterDecrypter(image)
    encrypter_decrypter.encrypt(message, bits_per_pixel)

    output_path = f"{event_ts}.png"

    success = cv2.imwrite(output_path, image, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    if not success:
        raise Exception(f"Couldn't save image at '{output_path}'")

    output_path = upload(output_path, remove_source=True)
    return make_response(image=output_path)


@bot_command("whoami")
def get_user_id(user) -> Response:
    """Show your user id. Format: '\\whoami'"""
    return make_response(text=user)


@bot_command  # type: ignore
def dec(files) -> Response:
    """Decrypt the text from the image. Format: '\\dec' + {image}"""
    image = get_image_from_files(files)
    decrypter = EncrypterDecrypter(image)
    message = decrypter.decrypt()
    return make_response(text=message)


@bot_command  # type: ignore
def enc(event_ts, text, files) -> Response:
    """Encrypt the text into the image. Format: '\\enc [text]' + {image}"""
    image = get_image_from_files(files)
    new_output = encode_and_move(event_ts, image, text)
    return new_output


@bot_command  # type: ignore
def enc_adv(event_ts, text: str, files: list[str]) -> Response:
    """Encrypt the text into the image. Format: '\\enc [1-8] [text]' + {image}"""
    match = re.findall("^[1-8]", text)
    bpp_as_str = match[0]
    bpp = int(bpp_as_str)
    text = text[len(bpp_as_str) :].strip()
    image = get_image_from_files(files)
    return encode_and_move(event_ts, image, text, bpp)
