import streamlit as st

def is_stackoverflow_link(link):
    return link.startswith("https://stackoverflow.com/users/")

def main():
    st.title("Please provide a link to your Stack Overflow account for verification")
    stackoverflow_link = st.text_input("Enter your Stack Overflow account link:")

    if stackoverflow_link:
        if is_stackoverflow_link(stackoverflow_link):
            st.write("Your Stack Overflow account link is:", stackoverflow_link)
        else:
            st.warning("This is not a valid Stack Overflow account link. Please enter a valid link.")
            st.text("Example: https://stackoverflow.com/users/1234567/your-username")

if __name__ == "__main__":
    main()
