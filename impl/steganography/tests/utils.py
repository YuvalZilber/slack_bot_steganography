import os
import re

import cv2

from impl.steganography.samples import StegSimpleImageEncrypterDecrypter as EncrypterDecrypter


def decrypt(image_path):
    image = cv2.imread(image_path)
    decrypter = EncrypterDecrypter(image)
    return decrypter.decrypt()


def encrypt(image_path, message, bits_per_pixel=1, output_path=None):
    image = cv2.imread(image_path)

    ed = EncrypterDecrypter(image)
    ed.encrypt(message, bits_per_pixel)

    new_path = output_path or re.sub("\.(\w{3,4})$", "_stego.png", image_path)
    if os.path.exists(new_path):
        os.remove(new_path)
    success = cv2.imwrite(new_path, image, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    if not success:
        raise Exception(f"Couldn't save image at '{new_path}'")
    return new_path
