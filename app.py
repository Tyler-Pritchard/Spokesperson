import os
import logging
import openai
from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up logging
if not os.path.exists('logs'):
    os.mkdir('logs')

logging.basicConfig(filename='logs/app.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Initialize Flask app
app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/test_openai')
def test_openai():
    try:
        # Create a simple message list to pass to ChatCompletion
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]

        # Call OpenAI's ChatCompletion API using the correct syntax
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access to GPT-4
            messages=messages,
            max_tokens=50
        )

        # Extract the response from the ChatCompletion
        answer = response['choices'][0]['message']['content'].strip()
        return jsonify({"prompt": "What is the capital of France?", "response": answer})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
