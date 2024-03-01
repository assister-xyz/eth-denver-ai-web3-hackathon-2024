import requests
import os
import hashlib
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import redis
from config import (
    OUTPUT_DIRECTORY
)
load_dotenv()

STACK_EXCHANGE_API_KEY = os.getenv("STACK_EXCHANGE_API_KEY")

def fetch_stackoverflow_questions(tag):
    api_url = "https://api.stackexchange.com/2.3/questions"
    
    params = {
        "pagesize": 100,  
        "order": "desc",
        "sort": "creation",
        "tagged": tag,
        "site": "stackoverflow",
        "filter": "withbody",  
        "key": STACK_EXCHANGE_API_KEY 
    }

    all_questions = []

    has_more = True
    page = 1

    try:
        while has_more:
            params["page"] = page
            response = requests.get(api_url, params=params)

            if response.status_code == 200:
                data = response.json()
                all_questions.extend(data["items"])

                has_more = data["has_more"]
                page += 1
            else:
                print("Error fetching questions:", response.status_code)
                print("Response:", response.text)
                break
    except Exception as e:
        print("Exception while fetching questions:", str(e))

    return all_questions[:10]

def get_accepted_answer(question_id):
    api_url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    
    params = {
        "pagesize": 10,  
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow",
        "filter": "withbody",  
        "key": STACK_EXCHANGE_API_KEY  
    }

    try:
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            if len(data["items"]) > 0:
                accepted_answers = [a for a in data["items"] if a.get("is_accepted", False)]
                if accepted_answers:
                    print("Use accepted")
                    return accepted_answers[0]
                else:
                    print("Use first")
                    return data["items"][0]
        else:
            print("Error fetching answer for question:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("Exception while fetching answer:", str(e))
    
    return None


def process_body(body):
    soup = BeautifulSoup(body, 'html.parser')
    for code_tag in soup.find_all('code'):
        code_tag.string = f"```{code_tag.text}```"
    for li_tag in soup.find_all('li'):
        li_tag.string = f"- {li_tag.text}"
    return soup.get_text()

def create_dataframe(tag):
    data = []
    questions = fetch_stackoverflow_questions(tag)
    total_questions = len(questions)
    print("There are", total_questions, "questions")

    for i, question in enumerate(questions, 1):
        accepted_answer = get_accepted_answer(question["question_id"])
        if accepted_answer:
            question_author = question['owner']['link']
            question_text = process_body(question['body'])
            answer_author = accepted_answer['owner']['link']
            answer_text = process_body(accepted_answer['body'])
            content_hash = hashlib.sha256(f"{question_text}{answer_text}".encode()).hexdigest()

            data.append({
                'question_id': f"{question['question_id']}",
                'question_author': question_author,
                'question': question_text,
                'answer_author': answer_author,
                'answer': answer_text,
                'hash': content_hash
            })

        # Print progress
        print(f"Processed: {i}/{total_questions}", end="\r")

    print("\nProcessing complete.")

    df = pd.DataFrame(data)
    return df

def insert_dataframe_to_redis(df):
    r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
    for _, row in df.iterrows():
        question_id = row['question_id']
        r.set(question_id, row.to_json())

def save_dataframe_to_csv(df, filename):
    df.to_csv(filename, index=False)

def main():
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
        
    tag = "nearprotocol"
    df = create_dataframe(tag)
    filename = f"{tag}_data.csv"
    save_dataframe_to_csv(df, os.path.join(OUTPUT_DIRECTORY, filename))
    insert_dataframe_to_redis(df)
if __name__ == "__main__":
    main()
