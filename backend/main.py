from flask import Flask, jsonify, request, Response
import json
from openai import OpenAI
from pinecone import Pinecone
import os
from dotenv import load_dotenv
import redis
from utlis.prompt_templates import general_qa_prompt_template
from config import EMBEDDING_MODEL, TEMPERATURE
load_dotenv()

app = Flask(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_HOST = os.getenv('PINECONE_HOST')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')

pc = Pinecone(api_key=PINECONE_API_KEY)

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


def generate_stream(prompt):
    query_vector = get_embedding(prompt, model=EMBEDDING_MODEL)

    index = pc.Index(PINECONE_INDEX_NAME, host=PINECONE_HOST)
    query_results = index.query(vector=query_vector, top_k=3)

    results = []
    for result in query_results['matches']:
        most_similar_id = result['id']
        value_from_redis = get_redis_value_by_id(most_similar_id)
        results.append(value_from_redis)
    result_context = ''.join(results)
    
    general_prompt = general_qa_prompt_template.format(client="Near", user_query=prompt, contexts=result_context)
    client = OpenAI(api_key = OPENAI_API_KEY)

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": general_prompt
            }
        ],
        #temperature = TEMPERATURE,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield f"data: {json.dumps(chunk.choices[0].delta.content)}\n\n"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data['prompt']
    return Response(generate_stream(prompt), mimetype='text/event-stream')
if __name__ == '__main__':
    app.run(port=5000)
