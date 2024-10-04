from flask import Blueprint, jsonify, session, request  # type: ignore
from flask_limiter import Limiter  # type: ignore
from flask_limiter.util import get_remote_address  # type: ignore
from .models import User, ConversationLog
from . import db
import openai  # type: ignore

# Define the main blueprint for the application
main_bp = Blueprint('main', __name__)

# Set up a rate limiter for all routes
limiter = Limiter(key_func=get_remote_address)


@main_bp.route('/')
def index():
    """
    Root endpoint for the Spokesperson App.

    Returns:
    --------
    JSON response:
        A welcome message indicating that the app is running.
    """
    return jsonify({"message": "Welcome to the Spokesperson App!"})


@main_bp.route('/generate_response', methods=['POST'])
@limiter.limit("10 per minute")  # Limit API requests to prevent abuse
def generate_response():
    """
    Endpoint to generate a response using the OpenAI API.

    Expects:
    --------
    - A JSON body containing the key "user_input" with the user message.

    Returns:
    --------
    JSON response:
        - 'user_input': The original user input message.
        - 'summary': The AI-generated response summary.
        - 'error': Error message, if any exception occurs.

    Example:
    --------
    Request:
    {
        "user_input": "Hello, how are you?"
    }

    Response:
    {
        "user_input": "Hello, how are you?",
        "summary": "I'm doing great, thank you for asking!"
    }
    """
    try:
        # Extract user input from the POST request body
        user_input = request.json.get("user_input")
        if not user_input:
            return jsonify({"error": "No user input provided."}), 400

        # Retrieve the user ID from the session or default to 1 (for demo purposes)
        user_id = session.get('user_id', 1)

        # Store the user input in the ConversationLog table in the database
        new_message = ConversationLog(user_id=user_id, message=user_input)
        db.session.add(new_message)
        db.session.commit()

        # Generate a response using the OpenAI ChatCompletion API
        messages = [{"role": "user", "content": user_input}]
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=50)

        # Extract the response content
        ai_response = response['choices'][0]['message']['content'].strip()

        # Return a JSON response with the original input and AI-generated summary
        return jsonify({"user_input": user_input, "summary": ai_response})

    except openai.error.OpenAIError as oe:
        # Specific handling for OpenAI-related errors
        return jsonify({"error": f"OpenAI API Error: {str(oe)}"}), 500
    except Exception as e:
        # General error handling for unexpected issues
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
