import os
import logging
import openai
from flask import Flask, jsonify, request, session
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
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")  # Set Flask session secret key

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

# Define a list of questions for the conversation flow
CONVERSATION_FLOW = [
    "What's your favorite hobby?",
    "Do you prefer the mountains or the beach?",
    "What's your ideal vacation destination?",
    "Are you more of a morning person or a night owl?",
    "If you could have dinner with any historical figure, who would it be?"
]

# Route for starting a new conversation
@app.route('/start_conversation', methods=['POST'])
def start_conversation():
    # Reset the conversation state and step counter
    session['conversation'] = []
    session['step'] = 0

    # Return the first question to the user
    first_question = CONVERSATION_FLOW[0]
    app.logger.info("Starting new conversation. First question: " + first_question)
    return jsonify({"message": first_question})


# Route to process user input and manage conversation flow
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

        # Retrieve the current step from the session
        current_step = session.get('step', 0)

        # Store the user's response in the conversation history
        conversation = session.get('conversation', [])
        conversation.append({"role": "user", "content": user_input})
        session['conversation'] = conversation

        # If we are still within the predefined questions, move to the next one
        if current_step < len(CONVERSATION_FLOW) - 1:
            next_step = current_step + 1
            next_question = CONVERSATION_FLOW[next_step]
            session['step'] = next_step

            # Log the current state
            app.logger.info(f"Current step: {next_step}, Next question: {next_question}")

            # Return the next question in the conversation flow
            return jsonify({"user_input": user_input, "next_question": next_question})

        else:
            # If the predefined questions are completed, generate an AI summary
            messages = [
                {"role": "system", "content": "You are a helpful assistant."}
            ] + [{"role": "user", "content": entry['content']} for entry in conversation]

            # Generate a summary using OpenAI's ChatCompletion API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150
            )

            # Extract the AI's response from the result
            ai_response = response['choices'][0]['message']['content'].strip()
            app.logger.info(f"Generated AI Summary: {ai_response}")

            # Reset conversation state after completion
            session.pop('conversation', None)
            session.pop('step', None)

            # Return the AI summary as JSON
            return jsonify({"user_input": user_input, "summary": ai_response})

    except Exception as e:
        # Handle exceptions and return error messages
        app.logger.error(f"Error in /generate_response: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
