from config import EMBEDDING_ENCODING, MAX_EMBEDDING_TOKENS, OPENAI_API_KEY, EMBEDDING_MODEL, PINECONE_API_KEY, PINECONE_HOST, PINECONE_INDEX_NAME
import tiktoken
from openai import OpenAI, APIConnectionError
import pandas as pd
from pinecone import Pinecone


def check_openai_api_key(client):
    try:
        client.models.list()
    except APIConnectionError as e:
        return False
    else:
        return True

def get_embedding(text, client, model = EMBEDDING_MODEL):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def vectorize(df, api_key):
    vectorization_columns = ["Question_ID", "Question_Title", "Question_Body", "Tags", "Answer_Body"]
    temp_df = df[vectorization_columns]
    temp_df = temp_df.dropna()
    temp_df["Combined"] = (
    "Question Title:" + temp_df["Question_Title"].str.strip() + 
    "; Question: " + temp_df["Question_Body"].str.strip() +
    "; Tags:" + temp_df["Tags"].str.strip() +
    "; Answer: " + temp_df["Answer_Body"].str.strip()
    )
    encoding = tiktoken.get_encoding(EMBEDDING_ENCODING)
    temp_df["n_tokens"] = temp_df["Combined"].apply(lambda x: len(encoding.encode(x)))
    temp_df = temp_df[temp_df.n_tokens <= MAX_EMBEDDING_TOKENS]

    client = OpenAI(api_key = api_key)
    if not check_openai_api_key(client):
        return df
    temp_df['Embeddings'] = temp_df["Combined"].apply(lambda x: get_embedding(x, client, model=EMBEDDING_MODEL))
    df = pd.merge(df, temp_df[["Question_ID", "Combined", "Embeddings"]], on="Question_ID", how="left")

    return df
   


def flush_pinecone_db():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME, host=PINECONE_HOST)


    index.delete(delete_all=True)

def unsert_df_to_pinecone(df):
    temp_df = df.dropna()
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    temp_df['Embeddings'] = temp_df['Embeddings'].apply(eval)
    
    data_to_insert = [(str(idx), vector) for idx, vector in zip(temp_df["Question_ID"], temp_df['Embeddings'])]
    
    index = pc.Index(PINECONE_INDEX_NAME, host=PINECONE_HOST)
    
    batch_size = 100
    for i in range(0, len(data_to_insert), batch_size):
        batch = data_to_insert[i:i+batch_size]
        try:
            index.upsert(vectors=batch)
            print(f"Upserted batch {i//batch_size + 1}")
        except Exception as e:
            print(f"Error during upsert of batch {i//batch_size + 1}:", e)
    
    print("All batches upserted")
    return True

