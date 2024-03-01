from openai import OpenAI
import pandas as pd
import os
import tiktoken
from dotenv import load_dotenv
from config import EMBEDDING_MODEL, EMBEDDING_ENCODING, MAX_EMBEDDING_TOKENS
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def get_embedding(text, client, model = EMBEDDING_MODEL):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def vectorize(df):
    df = df[["question_id","question_author", "question", "answer_author", "answer"]]
    df = df.dropna()
    df["combined"] = (
        "Question: " + df.question.str.strip() + "; Answer: " + df.answer.str.strip()
    )
    encoding = tiktoken.get_encoding(EMBEDDING_ENCODING)
    df["n_tokens"] = df.combined.apply(lambda x: len(encoding.encode(x)))
    df = df[df.n_tokens <= MAX_EMBEDDING_TOKENS]


    client = OpenAI(api_key = OPENAI_API_KEY)

    df['embeddings'] = df.combined.apply(lambda x: get_embedding(x, client, model=EMBEDDING_MODEL))
    
    return df
