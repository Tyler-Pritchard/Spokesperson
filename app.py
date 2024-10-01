# app.py
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

if __name__ == '__main__':
    app.run(debug=True)

conversation_flow = [
    # Each item can be a dictionary containing the question and any follow-up logic
    {
        'id': 1,
        'question': "What do you love to do in your free time? Any hobbies or passions that make your heart sing?",
        'key': 'interests'
    },
    # Add more questions as needed
]