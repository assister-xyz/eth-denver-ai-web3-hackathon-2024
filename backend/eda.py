import redis
import pandas as pd

def retrieve_dataframe_from_redis():
    r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
    keys = r.keys()  # Get all keys in the database
    data = []
    print(keys)
    for key in keys:
        row = r.get(key)
        data.append(row)
    
    df = pd.DataFrame(data)
    return df

df_from_redis = retrieve_dataframe_from_redis()

print(df_from_redis)
