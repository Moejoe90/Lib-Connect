from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
ENV_PATH = Path(__file__)/".env"
load_dotenv(dotenv_path=ENV_PATH)

NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_URI = os.getenv("NEO4J_URI")

