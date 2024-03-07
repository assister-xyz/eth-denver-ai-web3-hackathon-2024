import streamlit as st
import pandas as pd
from utils.database import upsert_dataframe
import redis
from config import REDIS_HOST, REDIS_PORT
def database_manager_page():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    try:
        response = r.ping()
        if response == True:
            st.success("Connected to Redis")
        else:
            st.error("Failed connected to Redis")
    except Exception as e:
        st.error("Failed connected to Redis")
    uploaded_file = st.file_uploader("Upload CSV file for DataFrame", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(df)
        if st.button("Unsert Dataframe to Redis"):                
            if upsert_dataframe(df):
                st.success("Data upserted successfully")
            else:
                st.error("Some occured problem with upserting data")