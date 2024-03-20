import streamlit as st
import requests
import json
import os
from config import BACKEND_URL, CONTRIBUTOR_URL

def streamlit_chat(prompt, openai_api_key):
    headers = {
        "Content-Type": "application/json",
        "OpenAI-API-Key": openai_api_key,
    }
    data = {"prompt": prompt}
    
    response = requests.post(BACKEND_URL+"/chat", headers=headers, data=json.dumps(data), stream=True)
    if response.status_code == 200:
        message_placeholder = st.empty() 
        full_text = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')  
                json_data = json.loads(decoded_line.replace('data: ', ''))
                full_text += json_data  
                current_text = message_placeholder.write(full_text)  
                st.session_state['last_message'] = json_data
    elif response.status_code == 401:
        st.error("Unauthorized, Invalid OpenAI key")

def main():
    st.set_page_config(
        page_title="Assisterr Chat (ETH Denver 2024)",
        page_icon="",
        menu_items={}
    )
    st.title("Assisterr Chat (ETH Denver 2024)")
    prompt = st.text_input("Enter your question:")
    
    openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    
    col1, _, col2 = st.columns([0.3,0.4,0.3])
    with col1:
        chat_button_clicked = st.button("Send", use_container_width=True)
    with col2:
        st.link_button("Are You a contributor?", CONTRIBUTOR_URL, use_container_width=True)
    
    if chat_button_clicked:
        if not openai_api_key:
            st.error("OpenAI API Key is required.")
        else:
            streamlit_chat(prompt, openai_api_key)

if __name__ == "__main__":
    main()
