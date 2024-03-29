from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
from openai import OpenAI, AuthenticationError
from pinecone import Pinecone
import os
import redis
from utlis.prompt_templates import general_qa_prompt_template
from config import (EMBEDDING_MODEL, TEMPERATURE, TOP_K_VECTORS, OPEN_AI_LLM,
                    PINECONE_API_KEY, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD,
                    PINECONE_INDEX_NAME, PINECONE_HOST)

app = Flask(__name__)
CORS(app)

pc = Pinecone(api_key=PINECONE_API_KEY)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0, charset="utf-8", decode_responses=True)

def check_openai_api_key(client):
    try:
        client.models.list()
    except AuthenticationError as e:
        return False
    else:
        return True

def get_redis_value_by_id(most_similar_id):
    value = r.get(most_similar_id)
    if value is not None:
        return value
    else:
        return "Value not found in Redis"


def get_embedding(text, model, api_key):
    client = OpenAI(api_key=api_key)
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def generate_stream(prompt, api_key,):
    query_vector = get_embedding(prompt, model=EMBEDDING_MODEL, api_key=api_key)

    index = pc.Index(PINECONE_INDEX_NAME, host=PINECONE_HOST)
    query_results = index.query(vector=query_vector, top_k=TOP_K_VECTORS)

    results = []
    tags = []
    for result in query_results['matches']:
        most_similar_id = result['id']
        value_from_redis = json.loads(get_redis_value_by_id(most_similar_id))
        concatenated_string = (
            "Question Title: " + value_from_redis["Question_Title"].strip() +
            "; Question: " + value_from_redis["Question_Body"].strip() +
            "; Tags: " + value_from_redis["Tags"].strip() +
            "; Answer: " + value_from_redis["Answer_Body"].strip()
        )
        tags.append(value_from_redis["Tags"].strip())
        results.append(concatenated_string)
    result_context = ''.join(results)

    general_prompt = general_qa_prompt_template.format(tag=tags, user_query=prompt, contexts=result_context)

    client = OpenAI(api_key=api_key)

    stream = client.chat.completions.create(
        model=OPEN_AI_LLM,
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
        # temperature=TEMPERATURE,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield f"data: {json.dumps(chunk.choices[0].delta.content)}\n\n"


def generate_chat_completion(prompt, api_key):
    query_vector = get_embedding(prompt, model=EMBEDDING_MODEL, api_key=api_key)

    index = pc.Index(PINECONE_INDEX_NAME, host=PINECONE_HOST)
    query_results = index.query(vector=query_vector, top_k=TOP_K_VECTORS)

    results = []
    tags = []
    for result in query_results['matches']:
        most_similar_id = result['id']
        value_from_redis = json.loads(get_redis_value_by_id(most_similar_id))
        concatenated_string = (
            "Question Title: " + value_from_redis["Question_Title"].strip() +
            "; Question: " + value_from_redis["Question_Body"].strip() +
            "; Tags: " + value_from_redis["Tags"].strip() +
            "; Answer: " + value_from_redis["Answer_Body"].strip()
        )
        tags.append(value_from_redis["Tags"].strip())
        results.append(concatenated_string)
    result_context = ''.join(results)

    general_prompt = general_qa_prompt_template.format(tag=tags, user_query=prompt, contexts=result_context)

    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model=OPEN_AI_LLM,
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
        # temperature=TEMPERATURE,
    )
    return completion.choices[0].message.content


@app.route('/health')
def health_check():
    return "I am alive! But is CI/CD alive? Check CI/CD v2", 200


@app.route('/ping-redis')
def ping_redis():
    try:
        pong = r.ping()
        if pong:
            return "Redis is running!", 200
        else:
            return "Error pinging Redis", 500
    except Exception as e:
        return str(e), 500


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data['prompt']
    api_key = request.headers.get('OpenAI-API-Key')
    if not api_key:
        return jsonify({"error": "OpenAI API Key is missing in headers"}), 400

    client = OpenAI(api_key=api_key)
    if not check_openai_api_key(client):
        return jsonify({"error": "Invalid OpenAI API Key"}), 401

    return Response(generate_stream(prompt, api_key), mimetype='text/event-stream')


@app.route('/chat-completion', methods=['POST'])
def chat_no_stream():
    data = request.json
    prompt = data['prompt']
    api_key = request.headers.get('OpenAI-API-Key')
    if not api_key:
        return jsonify({"error": "OpenAI API Key is missing in headers"}), 400

    client = OpenAI(api_key=api_key)
    if not check_openai_api_key(client):
        return jsonify({"error": "Invalid OpenAI API Key"}), 401

    completion = generate_chat_completion(prompt, api_key)
    return jsonify({"response": completion})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
