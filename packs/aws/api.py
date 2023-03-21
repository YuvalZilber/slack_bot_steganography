import contextlib
import os.path

import boto3  # type: ignore

BUCKET = "yzbucket1"


@contextlib.contextmanager
def s3client():
    client = boto3.client("s3")
    try:
        yield client
    finally:
        client.close()


def download(image_name, output):
    with s3client() as s3:
        s3.download_file(Bucket=BUCKET, Key=image_name, Filename=output)


def upload(filepath, *, remove_source=False):
    with s3client() as s3:
        filename = os.path.basename(filepath)
        s3.upload_file(Filename=filepath, Bucket=BUCKET, Key=filename)
        if remove_source:
            os.remove(filepath)
        return s3.generate_presigned_url(
            "get_object", Params={"Bucket": BUCKET, "Key": filename}
        )


if __name__ == "__main__":
    url2 = upload("1679362044.231479.png")
    print(url2)
