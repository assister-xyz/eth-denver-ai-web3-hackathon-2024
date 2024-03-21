import redis
from config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT

def upsert_dataframe(df):
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    
    unserted_count = 0
    for _, row in df.iterrows():
        question_id = row['Question_ID']
        if r.set(question_id, row.to_json()):
            unserted_count += 1
    
    if unserted_count == len(df):
        return True
    else:
        return False
