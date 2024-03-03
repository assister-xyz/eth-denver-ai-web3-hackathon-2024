import streamlit as st
import pandas as pd
from utils.database import upsert_dataframe

def database_manager_page():
    uploaded_file = st.file_uploader("Upload CSV file for DataFrame", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(df)
        if st.button("Unsert Dataframe to Redis"):                
            if upsert_dataframe(df):
                st.success("Data upserted successfully")
            else:
                st.error("Some occured problem with upserting data")