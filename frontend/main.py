import streamlit as st
import requests
import json
import os
from config import BACKEND_URL

def streamlit_chat(prompt):
    url = BACKEND_URL
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt}
    
    response = requests.post(url+"/chat", headers=headers, data=json.dumps(data), stream=True)
    
    message_placeholder = st.empty() 
    full_text = ""
    for line in response.iter_lines():
        if line:

            decoded_line = line.decode('utf-8')  
            json_data = json.loads(decoded_line.replace('data: ', ''))
            full_text += json_data  
            current_text = message_placeholder.write(full_text)  
            st.session_state['last_message'] = json_data 

def main():
    st.set_page_config(
        page_title="Assisterr Chat (ETH Denver 2024)",
        page_icon="",
        menu_items={}
    )
    st.title("Assisterr Chat (ETH Denver 2024)")
    prompt = st.text_input("Enter your question:")
    if st.button("Send"):
        streamlit_chat(prompt)

if __name__ == "__main__":
    main()
