import urllib.request

import cv2  # type: ignore

from auth import SLACK_TOKEN

SUPPORTED_IMAGE_TYPES = ("jpg", "png")


def get_image_from_files(files):
    if not files:
        raise Exception("[ERROR] No image found in your message")
    files_amount = len(files)
    if files_amount > 1:
        raise Exception(
            f"[ERROR] Found {files_amount} in your message, please upload 1 image in each message"
        )
    file_dict = files[0]
    file_url: str = file_dict.get("url_private")

    extension = file_url.split(".")[-1]
    if extension not in SUPPORTED_IMAGE_TYPES:
        raise Exception("[ERROR] please, upload file with the correct extension")
    opener = urllib.request.build_opener()
    opener.addheaders = [("Authorization", f"Bearer {SLACK_TOKEN}")]
    urllib.request.install_opener(opener)
    filename = f"image.{extension}"
    urllib.request.urlretrieve(file_url, filename)
    return cv2.imread(filename)
