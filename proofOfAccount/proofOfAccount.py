import os

import streamlit as st
from web3 import Web3, HTTPProvider
from eth_account.messages import defunct_hash_message
from eth_account import Account
from Contributor import Contributor
from generator import generate_unique_random_string
from validateProfile import check_about_section
import streamlit.components.v1 as components

def is_stackoverflow_link(link):
    return link.startswith("https://stackoverflow.com/users/")



def main():
    contributors = []

    st.session_state.setdefault("generated_code", None)
    st.session_state.setdefault("newContributor", None)

    st.title("Register as contributor👤")
    st.write("Please provide a link to your Stack Overflow account for verification.")

    stackoverflow_link = st.text_input("Your Stack Overflow Profile Link:")

    if stackoverflow_link:
        if is_stackoverflow_link(stackoverflow_link):
            st.success("Success! Valid Stack Overflow link.")

            if st.button("Get Verification Code"):
                st.session_state.generated_code = None
                st.session_state.newContributor = Contributor(stackoverflow_link)
                st.session_state.newContributor.set_unique_code(generate_unique_random_string())
                if st.session_state.generated_code is None:
                    st.session_state.generated_code = st.session_state.newContributor.get_unique_code()

                st.write("Please, copy and paste this code into your Stack Overflow about section:")
                st.code(f"Contributor Code: {st.session_state.generated_code}")

            if st.button("Verify Profile"):
                if check_about_section(st.session_state.newContributor.stackoverflow_account_link,
                                       st.session_state.newContributor.get_unique_code()):
                    st.success("Success! Your profile has been registered as contributor.")

                    if st.button("Sign"):
                        open_sign_html()
                    contributors.append(st.session_state.newContributor)
                else:
                    st.error("Verification failed. Please try again.")
        else:
            st.warning("Invalid Stack Overflow account link. Please enter a valid link.")
            st.text("Example: https://stackoverflow.com/users/1234567/your-username")
    else:
        if len(stackoverflow_link) != 0:
            st.warning("Please enter a valid Stack Overflow account link.")
            st.text("Example: https://stackoverflow.com/users/1234567/your-username")


def open_sign_html():
    file_path = os.path.join(os.path.dirname(__file__), "sign.html")
    os.system(f"start {file_path}")

if __name__ == "__main__":
    main()
