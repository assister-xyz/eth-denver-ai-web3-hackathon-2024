from pinecone import Pinecone
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_HOST = os.getenv('PINECONE_HOST')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')
pc = Pinecone(api_key=PINECONE_API_KEY)

df = pd.read_csv('tags/nearprotocol_data_with_embeddings.csv')


index = pc.Index(PINECONE_INDEX_NAME, host=PINECONE_HOST)
print(pc.list_indexes())
print(df)

# # Ensure 'embeddings' column is a list of floats
df['embeddings'] = df['embeddings'].apply(eval)

# # Convert to list of tuples
data_to_insert = [(str(idx), vector) for idx, vector in zip(df.question_id, df['embeddings'])]
print(len(data_to_insert[0]))
index.upsert(vectors=data_to_insert)

print("Data inserted into Pinecone successfully.")
