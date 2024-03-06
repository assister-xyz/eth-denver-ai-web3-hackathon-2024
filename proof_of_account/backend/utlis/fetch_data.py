import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_question_upvotes(answer, tag):
    STACK_EXCHANGE_API_KEY = "Eh4eYLdKmWxNP5I7q15kKg(("
    question_id = answer['question_id']
    question_url = f"https://api.stackexchange.com/2.3/questions/{question_id}?order=desc&sort=activity&site=stackoverflow&filter=withbody"
    params = {"key": STACK_EXCHANGE_API_KEY}
    question_response = requests.get(question_url, params=params)
    question_data = question_response.json()
    if tag in question_data['items'][0]['tags']:
        return answer['score']
    return 0

def fetch_answer_upvotes_parallel(answers, tag):
    total_upvotes = 0
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_upvotes = {executor.submit(fetch_question_upvotes, answer, tag): answer for answer in answers}
        for future in as_completed(future_to_upvotes):
            total_upvotes += future.result()
            print(total_upvotes)
    return total_upvotes

def fetch_total_upvotes(user_id, tag):
    page = 1
    has_more = True
    total_upvotes = 0

    while has_more:
        url = f"https://api.stackexchange.com/2.3/users/{user_id}/answers?order=desc&sort=activity&site=stackoverflow&page={page}&pagesize=100"
        STACK_EXCHANGE_API_KEY = "Eh4eYLdKmWxNP5I7q15kKg(("
        params = {"key": STACK_EXCHANGE_API_KEY}

        response = requests.get(url, params=params)
        data = response.json()

        total_upvotes += fetch_answer_upvotes_parallel(data['items'], tag)
        
        has_more = data['has_more']
        page += 1

    return total_upvotes

# user_id = '1178806'
# tag = 'nearprotocol'
# total_upvotes = fetch_total_upvotes(user_id, tag)
# print(f"Total Upvotes for questions with tag '{tag}':", total_upvotes)
