import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
CONTRIBUTOR_URL = os.getenv("CONTRIBUTOR_URL", "")