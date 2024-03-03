import os
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
EMBEDDING_ENCODING = os.getenv("EMBEDDING_ENCODING")
TOP_K_VECTORS = int(os.getenv("TOP_K_VECTORS")) 
OPEN_AI_LLM = os.getenv("OPEN_AI_LLM")
TEMPERATURE = float(os.getenv("TEMPERATURE"))
