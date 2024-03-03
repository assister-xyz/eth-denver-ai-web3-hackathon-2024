import streamlit as st
import pandas as pd
import os
from utils.vectorization import vectorize,flush_pinecone_db, unsert_df_to_pinecone
from config import CSV_OUTPUT_DIRECTORY
from utils.dataframe import save_dataframe_to_csv
def vectorization_page():
    st.header("Vectorization Page")
    uploaded_file = st.file_uploader("Upload CSV file for DataFrame", type=["csv"])    
    if uploaded_file: 
        df = pd.read_csv(uploaded_file)
        st.write(df)
        if 'Embeddings' not in df.columns:
            if st.session_state.df_qa_with_vectors is not None:
                st.subheader("Dataframe with Embeddings")
                st.dataframe(st.session_state.df_qa_with_vectors)
                if st.button("Save DataFrame"):
                    save_dataframe_to_csv(st.session_state.df_qa_with_vectors, uploaded_file.name, CSV_OUTPUT_DIRECTORY)
                if st.button("Reset"):
                    st.session_state.df_qa_with_vectors = None
                    st.rerun()
            else:
                if st.button("Vectorize Data"):
                    st.session_state.df_qa_with_vectors = vectorize(df)
                    st.subheader("Dataframe with Embeddings")
                    st.dataframe(st.session_state.df_qa_with_vectors)
                    if st.button("Save DataFrame"):
                        save_dataframe_to_csv(st.session_state.df_qa_with_vectors, uploaded_file.name, CSV_OUTPUT_DIRECTORY)
        else:
            col1, col2 = st.columns(2)
            st.write("Csv has Embedding already")
            with col1:
                if st.button("Flush Pinecone db", use_container_width=True):
                    if st.button("Sure?", use_container_width=True):
                        flush_pinecone_db()
            with col2:
                if st.button("Upsert vectors into Pinecone", use_container_width=True):
                    if unsert_df_to_pinecone(df):
                        st.success("Vectors was successfully upserted to Pinecone")
                    else:
                        st.error("Problem occured while upserting vectors to Pinecone")


    else:
        st.warning("Please upload a CSV file.")
