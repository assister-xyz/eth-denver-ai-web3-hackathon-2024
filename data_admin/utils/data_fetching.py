from config import STACK_EXCHANGE_API_KEY
import requests
import threading
from utils.data_proccessing import process_body
def fetch_questions(tag, max_questions=None):
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
    page = 1 
    total_questions_fetched = 0

    try:
        while (not max_questions or total_questions_fetched < max_questions):
            params["page"] = page
            response = requests.get(api_url, params=params)

            if response.status_code == 200 and len(response.json()["items"]) != 0:
                data = response.json()
                fetched_questions = data["items"]
                total_questions_fetched += len(fetched_questions)
                all_questions.extend(fetched_questions)
                page += 1
            else:
                print("Error fetching questions:", response.status_code)
                print("Response:", response.text)
                break
    except Exception as e:
        print("Exception while fetching questions:", str(e))

    return all_questions[:max_questions] if max_questions else all_questions

def get_accepted_answer(api_key, question_id):
    api_url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    params = {
        "pagesize": 10,
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow",
        "filter": "withbody",
        "key": api_key
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200 and response.json()["items"]:
        data = response.json()["items"]
        accepted_answers = [a for a in data if a.get("is_accepted", False)]
        return accepted_answers[0] if accepted_answers else data[0]
    return None

def get_and_append_accepted_answer(api_key, question):
    accepted_answer = get_accepted_answer(api_key, question["question_id"])
    if accepted_answer is not None:
        question["accepted_answer"] = accepted_answer
        question["accepted_answer"]["body"] = process_body(question["accepted_answer"]["body"])
    else:
        question["accepted_answer"] = None



def fetch_questions_and_answers(tag, max_questions=None):
    fetched_questions = fetch_questions(tag, max_questions)
    if fetched_questions:
        threads = []
        for question in fetched_questions:
            thread = threading.Thread(target=get_and_append_accepted_answer, args=(STACK_EXCHANGE_API_KEY, question))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    return fetched_questions


