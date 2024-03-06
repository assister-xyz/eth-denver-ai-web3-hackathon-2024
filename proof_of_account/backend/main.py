from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import json

from utlis.fetch_data import fetch_total_upvotes

app = Flask(__name__)
CORS(app) 

@app.route('/verify-stackoverflow', methods=['POST'])
def verify_stackoverflow():
    data = request.get_json()
    stackoverflow_link = data.get('link')
    unique_code = data.get('code')
    if not stackoverflow_link:
        return jsonify({'error': 'Stack Overflow link is required'}), 400

    if not unique_code:
        return jsonify({'error': 'Unique code is required'}), 400

    response = requests.get(stackoverflow_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        about_section = soup.find('div', class_='js-about-me-content')
        if about_section:
            about_text = about_section.text
            myregex = f"Code: {unique_code}"
            code_present = re.search(myregex, about_text)
            return jsonify({'valid': code_present is not None}), 200
        else:
            return jsonify({'error': 'About section not found'}), 404
    else:
        return jsonify({'error': 'Failed to fetch the profile page'}), 500

@app.route('/total-upvotes', methods=['POST'])
def get_total_upvotes():
    data = request.get_json()
    user_id = data.get('user_id')
    tag = data.get('tag')

    if user_id is None or tag is None:
        return jsonify({'error': 'Missing user_id or tag parameter'}), 400

    total_upvotes = fetch_total_upvotes(user_id, tag)
    return jsonify({'total_upvotes': total_upvotes})

if __name__ == '__main__':
    app.run(debug=True)
