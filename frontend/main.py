import streamlit as st
import requests
import json

def streamlit_chat(prompt):
    url = "http://127.0.0.1:5000/chat"
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt}
    
    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
    
    message_placeholder = st.empty()  # Create an empty placeholder
    full_text = ""
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')  # Decode the line
            json_data = json.loads(decoded_line.replace('data: ', ''))
            full_text += json_data  # Parse the JSON data
            current_text = message_placeholder.write(full_text)  # Update the placeholder with the current chunk of text
            st.session_state['last_message'] = json_data  # Optional: Store the last message in session state for further use

def main():
    st.set_page_config(
        page_title="Assisterr Chat",
        page_icon="",
        menu_items={}
    )
    st.title("Assisterr Chat")
    prompt = st.text_input("Enter your question:")
    if st.button("Send"):
        streamlit_chat(prompt)

if __name__ == "__main__":
    main()
