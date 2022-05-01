import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import S3UploadFailedError
from pathlib import Path
from PIL import Image
from settings import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME
import requests
import logging
import tempfile
import io

logger = logging.getLogger(__name__)
ROOT = Path(__file__).parent.resolve()


class ImageManagement(object):

    def __init__(self):

        self.s3 = None
        self.temp_dir = None
        self.session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

    def download(self, image_url, image_name):
        # create temp directory to save a file in it
        self.temp_dir = tempfile.TemporaryDirectory()
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            im = Image.open(io.BytesIO(r.content))
            with self.temp_dir as tempdir:
                im.save(f"{tempdir}/{image_name}")
                self.upload(f"{tempdir}/{image_name}", BUCKET_NAME)
                print(tempdir)
            print(ROOT)

    def upload(self, image_name, bucket, object_name=None):
        self.s3 = self.session.client('s3')
        if object_name is None:
            object_name = image_name
        if self.s3 is not None:
            try:
                self.s3.upload_file(image_name, bucket, object_name)
                print(f"{image_name} has been uploaded to {BUCKET_NAME}")
            except S3UploadFailedError:
                raise

    def generate_link(self, method_param, method='get_object'):
        self.s3 = self.session.client('s3')
        if self.s3 is not None:
            try:
                url = self.s3.generate_presigned_url(
                    ClientMethod=method,
                    Params=method_param,
                    ExpiresIn=3600
                )
                logger.info(f"Got pre-signed URL: {url}")

            except ClientError:
                logger.exception(
                    f"Couldn't get a pre-signed URL for client method {method}")
                raise
            print(url)
            return url
