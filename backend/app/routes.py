from flask import Blueprint, jsonify, session, request # type: ignore
from flask_limiter import Limiter # type: ignore
from flask_limiter.util import get_remote_address # type: ignore
from .models import User, ConversationLog
from . import db
import openai # type: ignore
import traceback

main_bp = Blueprint('main', __name__)
limiter = Limiter(key_func=get_remote_address)

@main_bp.route('/')
def index():
    return jsonify({"message": "Welcome to the Spokesperson App!"})

@main_bp.route('/generate_response', methods=['POST'])
def generate_response():
    try:
        user_input = request.json.get("user_input")
        user_id = session.get('user_id', 1)

        # Store the user input in the database
        new_message = ConversationLog(user_id=user_id, message=user_input)
        db.session.add(new_message)
        db.session.commit()

        # Generate response with OpenAI
        messages = [{"role": "user", "content": user_input}]
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=50)
        ai_response = response['choices'][0]['message']['content'].strip()

        return jsonify({"user_input": user_input, "summary": ai_response})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
