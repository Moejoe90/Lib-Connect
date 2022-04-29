from pathlib import Path
from PIL import Image
from settings import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME
import requests
import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import S3UploadFailedError
import logging
import tempfile
import io

logger = logging.getLogger(__name__)
ROOT = Path(__file__).parent.resolve()


class ImageManagement(object):

    def __init__(self):

        self.s3 = None
        self.session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        self.temp_dir = tempfile.TemporaryDirectory()

    def download(self, image_url, image_name):
        # create temp directory to save a file in it
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            im = Image.open(io.BytesIO(r.content))
            im.save(f"{self.temp_dir}/{image_name}")
            print(self.temp_dir)
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
        # TODO return s3 url

    # TODO generate small link from the real AWS image link
    def link_image(self):
        pass
