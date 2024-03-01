import streamlit as st
import requests
from config import API_ENDPOINT, DEFAULT_QUESTION

def get_rag_response(question):
    payload = {
        "query": question
    }

    responses = requests.post(API_ENDPOINT, json=payload)
    return responses.json()


def main():
    st.title("Assister Bot")
    st.session_state.setdefault("answer", None)
    st.session_state.setdefault("answer_keys", ["message", "redis"])

    question = st.text_input("Enter your question:", DEFAULT_QUESTION)

    if st.button("Ask"):
        with st.spinner("Thinking..."):
            st.session_state.answer = get_rag_response(question)
            if st.session_state.answer is not None:
                result = st.session_state.answer["message"]
                st.write(result)

if __name__ == "__main__":
    main()
