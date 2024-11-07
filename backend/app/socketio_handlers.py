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
        
        # Initialize session data for user_id, conversation_stage, and user_data
        if 'user_id' not in session:
            session['user_id'] = 1
        session['conversation_stage'] = 0
        session['user_data'] = {}

        # Welcome message and initial question
        emit('response', {'id': '0', 'message': 'Welcome! You are now connected to the server.'})
        first_question = get_next_question(session['conversation_stage'])
        emit('response', {'id': '0', 'message': first_question['question']})

    @socketio.on('message')
    def handle_message(data):
        """Handles incoming messages from WebSocket clients."""
        try:
            user_id = session.get('user_id', 1)
            conversation_stage = session.get('conversation_stage', 0)
            user_data = session['user_data']

            # Log and save the user's message
            app.logger.info(f"Message received from user {user_id}: {data}")
            new_message = ConversationLog(user_id=user_id, message=data)
            db.session.add(new_message)
            db.session.commit()
            app.logger.info(f"Message {new_message.id} saved to the database.")

            # Store user response for each stage based on conversation flow
            if conversation_stage == 0:
                user_data['name'] = data
            elif conversation_stage == 1:
                user_data['age'] = data
            elif conversation_stage == 2:
                user_data['gender'] = data
            elif conversation_stage == 3:
                user_data['hobby'] = data
            
            # Generate response based on user input and conversation stage
            if conversation_stage < 3:
                session['conversation_stage'] += 1
                next_question = get_next_question(session['conversation_stage'])
                emit('response', {'id': str(new_message.id), 'message': next_question['question']})
            else:
                # If all questions are answered, generate a summary
                summary = generate_facilitator_response(user_data)
                emit('response', {'id': str(new_message.id), 'message': summary})

        except Exception as e:
            app.logger.error(f"Error handling message for user {user_id}: {str(e)}")
            emit('response', {'id': '0', 'message': f"An error occurred: {str(e)}"})

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handles a WebSocket client disconnection."""
        app.logger.info("Client disconnected from WebSocket")
