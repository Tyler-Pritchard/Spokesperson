import os
import logging
from flask_cors import CORS # type: ignore
import openai # type: ignore
from flask import Flask, jsonify, request, session # type: ignore
from flask_socketio import SocketIO, emit # type: ignore
from dotenv import load_dotenv # type: ignore
from openai.error import OpenAIError # type: ignore
from flask_limiter import Limiter # type: ignore
from flask_limiter.util import get_remote_address # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from datetime import datetime

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spokesperson.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app)

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the database
db = SQLAlchemy(app)

# Initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Set up rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]  # Limit to 5 API calls per minute per IP address
)


# Models for User and ConversationLog
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class ConversationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('conversations', lazy=True))

# Create all database tables
with app.app_context():
    db.create_all()
    

# Root route for basic testing
@app.route('/')
def index():
    app.logger.info("Index route accessed")
    return jsonify({"message": "Welcome to the Spokesperson App!"})


# WebSocket event handler for client connections
@socketio.on('connect')
def handle_connect():
    app.logger.info("Client connected via WebSocket")
    print("Client connected via WebSocket")  # Print for quick visibility
    emit('response', {'message': 'Welcome! You are now connected to the server.'})

# WebSocket event handler for receiving messages
@socketio.on('message')
def handle_message(data):
    app.logger.info(f"Message received via WebSocket: {data}")
    print(f"Message received via WebSocket: {data}")  # Print for quick visibility
    emit('response', {'message': f"Server received: {data}"}, broadcast=True)

# WebSocket event handler for disconnection
@socketio.on('disconnect')
def handle_disconnect():
    app.logger.info("Client disconnected from WebSocket")
    print("Client disconnected from WebSocket")  # Print to console for quick visibility
    
@socketio.on_error()        # Handles any uncaught errors in SocketIO
def error_handler(e):
    app.logger.error(f"SocketIO Error: {str(e)}")


# Define a simple test route for OpenAI
@app.route('/test_openai')
def test_openai():
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=50
        )
        answer = response['choices'][0]['message']['content'].strip()
        app.logger.info(f"OpenAI Response: {answer}")
        return jsonify({"prompt": "What is the capital of France?", "response": answer})
    except Exception as e:
        app.logger.error(f"Error in test_openai: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    
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
@limiter.limit("3 per minute")  # Apply a specific rate limit for starting a conversation
def start_conversation():
    try:
        # Create a new user profile (for demo purposes, username is hardcoded)
        new_user = User(username="DemoUser")
        db.session.add(new_user)
        db.session.commit()

        # Store user ID in session
        session['user_id'] = new_user.id

        # Return the first question to the user
        first_question = CONVERSATION_FLOW[0]
        app.logger.info("Starting new conversation. First question: " + first_question)
        return jsonify({"message": first_question})

    except Exception as e:
        app.logger.error(f"Error starting conversation: {str(e)}")
        return jsonify({"error": "Failed to start a new conversation. Please try again."}), 500


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
        
        # Retrieve the user ID
        user_id = session.get('user_id')
        if not user_id:
            app.logger.error("User ID not found in session")
            return jsonify({"error": "User session is not active."}), 400

        # Store the user response in the database
        new_message = ConversationLog(user_id=user_id, message=user_input)
        db.session.add(new_message)
        db.session.commit()

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

    except OpenAIError as oe:
        app.logger.error(f"OpenAI API Error: {str(oe)}")
        return jsonify({"error": "OpenAI API request failed. Please try again later."}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error in /generate_response: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
    
# Start the Flask-SocketIO server
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
