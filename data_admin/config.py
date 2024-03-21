import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CSV_OUTPUT_DIRECTORY = os.getenv('CSV_OUTPUT_DIRECTORY', 'data_output')

STACK_EXCHANGE_API_KEY = os.getenv("STACK_EXCHANGE_API_KEY")

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_HOST = os.getenv('PINECONE_HOST')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'default-model')
EMBEDDING_ENCODING = os.getenv('EMBEDDING_ENCODING', 'default-encoding')
MAX_EMBEDDING_TOKENS = int(os.getenv('MAX_EMBEDDING_TOKENS', 512))

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', "")