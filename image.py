from pathlib import Path
from PIL import Image
from settings import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME
import requests
import boto3
from botocore.exceptions import ClientError
import logging
import tempfile
import io

logger = logging.getLogger(__name__)
ROOT = Path(__file__).parent


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

    # TODO upload the image to the AWS
    def upload(self):
        pass

    # TODO generate small link from the real AWS image link
    def link_image(self):
        pass
