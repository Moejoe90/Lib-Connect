from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
ENV_PATH = Path(__file__)/".env"
load_dotenv(dotenv_path=ENV_PATH)

# load auth for actual database
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_URI = os.getenv("NEO4J_URI")

# load auth for sandbox database
TEST_USER = os.getenv("TEST_USER")
TEST_URI = os.getenv("TEST_URI")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


# load auth for AWS S3
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")
