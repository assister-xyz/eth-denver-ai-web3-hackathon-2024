from pinecone import Pinecone
import os
import pandas as pd
from dotenv import load_dotenv

def insert_df_to_pinecone(df):
    load_dotenv()
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_HOST = os.getenv('PINECONE_HOST')
    PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')

    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    df['embeddings'] = df['embeddings'].apply(eval)
    
    data_to_insert = [(str(idx), vector) for idx, vector in zip(df.question_id, df['embeddings'])]
    
    index = pc.Index(PINECONE_INDEX_NAME, host=PINECONE_HOST)

    index.upsert(vectors=data_to_insert)
    
    try:
        index.upsert(vectors=data_to_insert)
        print("Data inserted into Pinecone successfully.")
        return True
    except Exception as e:
        print("Error inserting data into Pinecone:", e)
        return False
