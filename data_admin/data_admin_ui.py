import os
import streamlit as st
import pandas as pd
from crawler import (
    fetch_stackoverflow_questions,
    get_accepted_answer,
    process_body,
    create_dataframe,
    insert_dataframe_to_redis,
    save_dataframe_to_csv
)
from vectorize import vectorize
from insert_vectors import insert_df_to_pinecone
from config import OUTPUT_DIRECTORY
import re


def fetch_questions(tag, max_question):
    fetched_questions = fetch_stackoverflow_questions(tag, max_question)
    st.session_state.fetched_questions = fetched_questions
    st.write(f"Total Questions: {len(fetched_questions)}")

    # Progress bar
    progress_bar = st.progress(0)
    progress_text = st.empty()

    with st.expander("Questions"):
        for i, question in enumerate(fetched_questions):
            progress_percent = (i + 1) / len(fetched_questions)
            progress_bar.progress(progress_percent)
            progress_text.text(f"Processing question {i+1}/{len(fetched_questions)}")

            st.write("Question:", process_body(question['body']))
            # accepted_answer = get_accepted_answer(question['question_id'])
            # if accepted_answer:
            #     st.write("Accepted Answer:", process_body(accepted_answer['body']))
            st.write("---")

    progress_bar.empty()
    progress_text.empty()

def create_display_dataframe(questions):
    df_with_answers, df_without_answers = create_dataframe(questions)
    st.session_state.df_with_answers = df_with_answers
    st.session_state.df_without_answers = df_without_answers
    st.subheader("DataFrame with Answers")
    st.write(df_with_answers)
    st.subheader("DataFrame without Answers")
    st.write(df_without_answers)

def save_to_csv(tag, df_with, df_without):
    filename_with = f"{tag}_data.csv"
    filename_without = f"{tag}_questions.csv"
    save_dataframe_to_csv(df_with, os.path.join(OUTPUT_DIRECTORY, filename_with))
    save_dataframe_to_csv(df_without, os.path.join(OUTPUT_DIRECTORY, filename_without))
    st.write("DataFrames saved as CSV")

def insert_to_redis(df_with):
    insert_dataframe_to_redis(df_with)
    st.write("Data inserted into Redis")

def vectorization(df):
    pass

def main():
    st.title('Data admin page')
    st.session_state.setdefault("fetched_questions", None)
    st.session_state.setdefault("df_with_answers", None)
    st.session_state.setdefault("df_without_answers", None)

    pages = ["Crawling", "Upsert Redis", "Vectorization","Upsert Vectors"]
    page = st.sidebar.radio("Select Page", pages)

    if page == "Crawling":
        st.header("Crawling")
        tag = st.text_input("Enter Tag (e.g., python):", "nearprotocol")
        max_question = st.number_input("Max Questions:", min_value = 1, step=1, value=10)

        if st.button("Fetch Questions"):
            fetch_questions(tag, max_question)

        if st.button("Create and Display DataFrame"):
            create_display_dataframe(st.session_state.fetched_questions)

        if st.button("Save to CSV"):
            if st.session_state.df_with_answers is not None and st.session_state.df_without_answers is not None:
                save_to_csv(tag, st.session_state.df_with_answers, st.session_state.df_without_answers)
            else:
                st.write("Please fetch questions and create DataFrame first.")

        
    elif page == "Upsert Redis":
        uploaded_file = st.file_uploader("Upload CSV file for DataFrame", type=["csv"])
        if uploaded_file:
            temp_df = pd.read_csv(uploaded_file)
            st.write(temp_df)
            if st.button("Insert to Redis"):                
                insert_to_redis(temp_df)
    elif page == "Vectorization":
        st.header("Vectorization Page")
        uploaded_file = st.file_uploader("Upload CSV file for DataFrame", type=["csv"])
        if uploaded_file:
            filename = re.match(r'(.+)\..+', uploaded_file.name).group(1)
            temp_df = pd.read_csv(uploaded_file)
            st.write(temp_df) 
            if st.button("Vectorize Data"):
                df_with_vectors = vectorize(temp_df)
                st.write(df_with_vectors["embeddings"])
                df_with_vectors.to_csv(os.path.join(OUTPUT_DIRECTORY, filename) + '_with_embeddings.csv', index=False)

    elif page == "Upsert Vectors":
        st.header("Upsert Vectors Page")
        uploaded_file = st.file_uploader("Upload CSV file for DataFrame", type=["csv"])
        if uploaded_file:
            temp_df = pd.read_csv(uploaded_file)
            st.write(temp_df)
            if st.button("Upsert Vector"):
                if insert_df_to_pinecone(temp_df):
                    st.success("Data upserted successfully!")
                else:
                    st.error("Failed to upsert data into db")

if __name__ == "__main__":
    main()
