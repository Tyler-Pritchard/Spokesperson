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
from flask_session import Session # type: ignore
import sqlalchemy # type: ignore
from datetime import datetime
import traceback

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

sqlalchemy.echo = True

# Initialize Flask app
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")  # Set Flask session secret key
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spokesperson.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Enable CORS
CORS(app)

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
print(f"Current OpenAI API Key: {openai.api_key}")

# Initialize the database
db = SQLAlchemy(app)

# Initialize Flask-SocketIO
Session(app)
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)

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
    print("Client connected via WebSocket")

    # Set a default user ID for the session if not set (for demo purposes)
    if 'user_id' not in session:
        session['user_id'] = 1  # Hardcode for testing/demo purposes
        app.logger.info("User ID set to 1 for session.")
    
    emit('response', {'id':'0', 'message': 'Welcome! You are now connected to the server.'})

    
    
def generate_facilitator_response(user_id):
    try:
        # Retrieve the previous conversation messages for this user
        conversation_logs = ConversationLog.query.filter_by(user_id=user_id).order_by(ConversationLog.timestamp).all()
        conversation_text = "\n".join([f"User: {log.message}" for log in conversation_logs])

        # Debug: Log the conversation history
        app.logger.info(f"Conversation history for user {user_id}:\n{conversation_text}")

        # Prepare the prompt for GPT-3
        prompt = (
            f"You are a helpful AI Facilitator guiding a user to build a personalized chatbot profile. "
            f"Based on the conversation so far, ask a relevant follow-up question or provide insightful commentary.\n\n"
            f"Previous Conversation:\n{conversation_text}\n\n"
            f"Facilitator: "
        )

        # Debug: Log the generated prompt
        app.logger.info(f"Generated prompt for GPT-3:\n{prompt}")

        # Generate a response using OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=["User:"]
        )

        # Debug: Log the raw response from OpenAI
        app.logger.info(f"OpenAI response:\n{response}")

        facilitator_response = response.choices[0].text.strip()
        return facilitator_response

    except OpenAIError as oe:
        app.logger.error(f"OpenAI API Error: {str(oe)}")
        return "Sorry, I'm having trouble generating a response. Please try again."
    except Exception as e:
        app.logger.error(f"Unexpected error in generate_facilitator_response: {str(e)}")
        return "Sorry, I'm having trouble generating a response. Please try again."



# WebSocket event handler for receiving messages
@socketio.on('message')
def handle_message(data):
    app.logger.info(f"Message received via WebSocket: {data}")
    print(f"Message received via WebSocket: {data}")

    # Retrieve the user ID from the session
    user_id = session.get('user_id', 1)
    if not user_id:
        app.logger.error("User ID not found in session during WebSocket message handling.")
        emit('response', {'id':'0', 'message': 'Error: User session is not active.'})
        return

    # Store the WebSocket message in the database
    try:
        new_message = ConversationLog(user_id=user_id, message=data)
        db.session.add(new_message)
        db.session.commit()
        print(f"Message {new_message.id} committed to database")

        app.logger.info(f"Message saved to database: {new_message}")

        # Generate a GPT-based response using the conversation history
        ai_response = generate_facilitator_response(user_id)
        if ai_response:
            response_data = {'id': str(new_message.id), 'message': ai_response}
        else:
            response_data = {'id': str(new_message.id), 'message': 'Sorry, I couldn’t process your request.'}

    except Exception as e:
        app.logger.error(f"Error saving WebSocket message to database: {str(e)}")
        emit('response', {'message': 'Error saving message to the database.'})
        return

    # Emit the GPT-generated response back to the client
    print(f"Emitting response: {response_data}")
    emit('response', response_data, broadcast=True)



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
    "What would you like your username to be?"
    "What's your favorite hobby?",
    "Do you prefer the mountains or the beach?",
    "What's your ideal vacation destination?",
    "Are you more of a morning person or a night owl?",
    "If you could have dinner with any historical figure, who would it be?"
]



@app.route('/get_conversation', methods=['GET'])
def get_conversation():
    # user_id = session.get('user_id')
    user_id = 1
    if not user_id:
        app.logger.error("User session is not active.")
        return jsonify({"error": "User session is not active."}), 400

    try:
        conversation_logs = ConversationLog.query.filter_by(user_id=user_id).all()
        messages = [{"id": str(index), "message": log.message} for index, log in enumerate(conversation_logs)]
        app.logger.info(f"Conversation history for user {user_id}: {messages}")
        return jsonify({"conversation": messages})
    except Exception as e:
        app.logger.error(f"Error retrieving conversation: {str(e)}")
        return jsonify({"error": "Failed to retrieve conversation history."}), 500




@app.route('/start_conversation', methods=['POST'])
@limiter.limit("3 per minute")  # Apply a specific rate limit for starting a conversation
def start_conversation():
    try:
        # Check if a user with the username already exists
        existing_user = User.query.filter_by(username="DemoUser").first()
        if existing_user:
            # If the user already exists, set the session to the existing user ID
            session['user_id'] = existing_user.id
            app.logger.info(f"Existing user found: {existing_user.username}. Using existing user ID: {existing_user.id}")
        else:
            # Create a new user profile (for demo purposes, username is hardcoded)
            new_user = User(username="DemoUser")
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            app.logger.info(f"New user created: {new_user.username}. New user ID: {new_user.id}")

        # Log the session state
        app.logger.info(f"Session after starting conversation: {session}")

        # Return the first question to the user
        first_question = CONVERSATION_FLOW[0]
        app.logger.info("Starting new conversation. First question: " + first_question)
        return jsonify({"message": first_question})

    except Exception as e:
        app.logger.error(f"Error starting conversation: {str(e)}")
        return jsonify({"error": "Failed to start a new conversation. Please try again."}), 500


# Route to add test data for database testing
@app.route('/add_test_data')
def add_test_data():
    try:
        # Check if the user already exists
        existing_user = User.query.filter_by(username="TestUser").first()
        if existing_user:
            return jsonify({"message": f"User {existing_user.username} already exists!"})

        # If not, create a new user
        new_user = User(username="TestUser")
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": f"Test user {new_user.username} added successfully!"})

    except Exception as e:
        app.logger.error(f"Error adding test data: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/generate_response', methods=['POST'])
def generate_response():

    try:
        app.logger.info("generate_response route accessed.")
        app.logger.info(f"Session Data: {session}")

        # Get user input from the POST request
        user_input = request.json.get("user_input")
        
        # If no input is provided, return an error message
        if not user_input:
            app.logger.warning("No user input provided in /generate_response")
            return jsonify({"error": "No user input provided."}), 400

        # Retrieve the user ID (ensure it defaults to a known value for now)
        user_id = session.get('user_id', 1)
        if not user_id:
            app.logger.error("User ID not found in session")
            return jsonify({"error": "User session is not active."}), 400

        # Store the user response in the database
        new_message = ConversationLog(user_id=user_id, message=user_input)
        db.session.add(new_message)
        db.session.commit()
        app.logger.info(f"Message {new_message.id} committed to database")

        # Build the message history
        conversation_logs = ConversationLog.query.filter_by(user_id=user_id).order_by(ConversationLog.timestamp).all()
        messages = [{"role": "system", "content": "You are a helpful assistant."}]

        # Add all previous user inputs to the message history
        for log in conversation_logs:
            messages.append({"role": "user", "content": log.message})

        # Add the most recent user input
        messages.append({"role": "user", "content": user_input})

        # Debugging: Print out the entire message history for verification
        print(f"Requesting OpenAI with the following messages:\n{messages}")
        app.logger.info(f"Messages sent to OpenAI: {messages}")

        # Make the OpenAI API call
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150
            )
            app.logger.info(f"OpenAI Response: {response}")
        except openai.error.OpenAIError as oe:
            app.logger.error(f"OpenAI Error during request: {str(oe)}")
            return jsonify({"error": f"OpenAI API request failed: {str(oe)}"}), 500

        # Check if the response contains choices and is structured correctly
        if 'choices' not in response or len(response['choices']) == 0:
            app.logger.error(f"OpenAI returned an unexpected response: {response}")
            return jsonify({"error": "OpenAI API returned an empty response. Please try again later."}), 500

        # Extract the AI's response from the result
        ai_response = response['choices'][0]['message']['content'].strip()
        app.logger.info(f"Generated AI Summary: {ai_response}")

        # Return the AI summary as JSON
        return jsonify({"user_input": user_input, "summary": ai_response})

    except openai.error.OpenAIError as oe:
        app.logger.error(f"OpenAI API Error: {str(oe)}")
        return jsonify({"error": f"OpenAI API request failed: {str(oe)}"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error in /generate_response: {str(e)}")
        app.logger.error(traceback.format_exc())  # Log the stack trace for debugging
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    
# Start the Flask-SocketIO server
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
