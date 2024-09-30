import os
import logging
import openai
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up logging
if not os.path.exists('logs'):
    os.mkdir('logs')

logging.basicConfig(
    filename='logs/app.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Initialize Flask app
app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Root route for basic testing
@app.route('/')
def index():
    app.logger.info("Index route accessed")
    return jsonify({"message": "Welcome to the Spokesperson App!"})

# Existing test route to verify OpenAI connection
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
        app.logger.info(f"OpenAI Response: {answer}")
        return jsonify({"prompt": "What is the capital of France?", "response": answer})

    except Exception as e:
        app.logger.error(f"Error in test_openai: {str(e)}")
        return jsonify({"error": str(e)})

# New route to handle AI response generation
@app.route('/generate_response', methods=['POST'])
def generate_response():
    try:
        # Get user input from the POST request
        user_input = request.json.get("user_input")

        # If no input is provided, return an error message
        if not user_input:
            app.logger.warning("No user input provided in /generate_response")
            return jsonify({"error": "No user input provided."}), 400

        app.logger.info(f"User Input Received: {user_input}")

        # Create the AI prompt using the user input
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]

        # Generate a response using OpenAI's ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100
        )

        # Extract the AI's response from the result
        ai_response = response['choices'][0]['message']['content'].strip()
        app.logger.info(f"Generated AI Response: {ai_response}")

        # Return the AI response as JSON
        return jsonify({"user_input": user_input, "ai_response": ai_response})

    except Exception as e:
        # Handle exceptions and return error messages
        app.logger.error(f"Error in /generate_response: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
