from flask import session, request  # type: ignore
from flask_socketio import emit  # type: ignore
from .models import ConversationLog
from . import db
from .services import get_next_question, generate_facilitator_response

def register_socket_handlers(socketio, app):
    """
    Registers WebSocket event handlers for the Flask-SocketIO server.
    """

    @socketio.on('connect')
    def handle_connect():
        """Handles a new WebSocket client connection."""
        app.logger.info("Client connected via WebSocket")

        # Initialize user_id, conversation_stage, and user_data in the session
        if request and 'user_id' not in session:
            session['user_id'] = 1
        if 'conversation_stage' not in session:
            session['conversation_stage'] = 0
        if 'user_data' not in session:
            session['user_data'] = {}

        user_data = session['user_data']  # Use this for storing user responses

        # Send welcome message and the first question
        emit('response', {'id': '0', 'message': 'Welcome! You are now connected to the server.'})
        first_question = get_next_question(session['conversation_stage'], user_data)
        emit('response', {'id': '0', 'message': first_question['question']})

    @socketio.on('message')
    def handle_message(data):
        """
        Handles incoming messages from WebSocket clients.
        """
        try:
            user_id = session.get('user_id', 1)
            conversation_stage = session.get('conversation_stage', 0)
            user_data = session.get('user_data', {})

            app.logger.info(f"Message received from user {user_id}: {data}")
            
            # Save user response in user_data
            if conversation_stage == 0:
                user_data['name'] = data
            elif conversation_stage == 1:
                user_data['age'] = data
            elif conversation_stage == 2:
                user_data['gender'] = data
            elif conversation_stage == 3:
                user_data['hobby'] = data
            session['user_data'] = user_data  # Save to session

            # Log the message in the database
            new_message = ConversationLog(user_id=user_id, message=data)
            db.session.add(new_message)
            db.session.commit()
            app.logger.info(f"Message {new_message.id} saved to the database.")

            # Move to the next stage
            session['conversation_stage'] += 1
            next_question = get_next_question(session['conversation_stage'], user_data)
            
            # Check if we are at the end of the conversation
            if next_question["type"] == "end":
                emit('response', {'id': str(new_message.id), 'message': next_question["question"]})
                session['conversation_stage'] = 0  # Reset for new conversation
                session['user_data'] = {}  # Clear user data after summary
            else:
                emit('response', {'id': str(new_message.id), 'message': next_question["question"]})

        except Exception as e:
            app.logger.error(f"Error handling message for user {user_id}: {str(e)}")
            emit('response', {'id': '0', 'message': f"An error occurred: {str(e)}"})

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handles a WebSocket client disconnection."""
        app.logger.info("Client disconnected from WebSocket")
