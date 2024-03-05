import requests
from bs4 import BeautifulSoup
import re


def check_about_section(stackoverflow_link, unique_code):
    response = requests.get(stackoverflow_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        about_section = soup.find('div', class_='js-about-me-content')
        if about_section:
            about_text = about_section.text
            myregex = f"Contributor Code: {unique_code}"
            code_present = re.search(myregex, about_text)
            return code_present is not None
        else:
            print("About section not found.")
    else:
        print("Failed to fetch the profile page.")

#print(check_about_section("https://stackoverflow.com/users/16343464/mozway", "123"))