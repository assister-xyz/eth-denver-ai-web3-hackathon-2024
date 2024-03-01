from flask import Flask, jsonify, request
from openai import OpenAI
from pinecone import Pinecone
import os
from dotenv import load_dotenv
from transformers import BertModel, BertTokenizer
import torch
import redis
from utlis.prompt_templates import general_qa_prompt_template
from langchain.chains import LLMChain
from config import EMBEDDING_MODEL
load_dotenv()

app = Flask(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_HOST = os.getenv('PINECONE_HOST')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')

pc = Pinecone(api_key=PINECONE_API_KEY)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)


def get_redis_value_by_id(most_similar_id):
    value = r.get(most_similar_id)
    if value is not None:
        return value
    else:
        return "Value not found in Redis"


def get_embedding(text, model):
    client = OpenAI(api_key = OPENAI_API_KEY)
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def get_embedding_bert(text):
    encoded_input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        model_output = model(**encoded_input)

    embeddings = model_output.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings.tolist()


@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    query_text = data.get('query', '')

    query_vector = get_embedding(query_text, model=EMBEDDING_MODEL)

    index = pc.Index(PINECONE_INDEX_NAME, host=PINECONE_HOST)
    query_results = index.query(vector=query_vector, top_k=3)

    results = []
    for result in query_results['matches']:
        most_similar_id = result['id']
        value_from_redis = get_redis_value_by_id(most_similar_id)
        results.append(value_from_redis)
    result_context = ''.join(results)
    
    prompt = general_qa_prompt_template.format(client="Near", user_query=query_text, contexts=result_context)
    client = OpenAI(api_key = OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    response_message = response.choices[0].message.content
    return jsonify({"message": response_message, "redis": result_context})

if __name__ == '__main__':
    app.run(port=5000)
