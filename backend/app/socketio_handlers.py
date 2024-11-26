from flask import session, request  # type: ignore
from flask_socketio import emit  # type: ignore
from .models import ConversationLog
from . import db
from .services import CONVERSATION_FLOW, get_next_question, validate_input

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
        user_id = session.get('user_id', 1)
        conversation_stage = session.get('conversation_stage', 0)
        user_data = session.get('user_data', {})
        new_message = None

        try:
            app.logger.info(f"Message received from user {user_id}: {data}")

            # Save user response in user_data based on the current stage
            if conversation_stage < len(CONVERSATION_FLOW):
                question_data = CONVERSATION_FLOW[conversation_stage]
                input_type = question_data["type"]
                key = question_data["key"]
                options = question_data.get("options", None)

                # Validate input
                if not validate_input(data, input_type, options):
                    emit('response', {'id': '0', 'message': f"Invalid input for {question_data['question']}."})
                    return

                # Save valid data
                user_data[key] = data
                session['user_data'] = user_data  # Update session data
                app.logger.info(f"Updated user_data: {user_data}")

            # Log the message in the database
            new_message = ConversationLog(user_id=user_id, message=data)
            db.session.add(new_message)
            db.session.commit()
            app.logger.info(f"Message {new_message.id} saved to the database.")

            # Move to the next stage and fetch the next question
            session['conversation_stage'] += 1
            next_question = get_next_question(session['conversation_stage'], user_data)

            # Check if we are at the end of the conversation
            if next_question["type"] == "end":
                emit('response', {'id': str(new_message.id), 'message': next_question["question"]})
                # Reset the session for a new conversation
                session['conversation_stage'] = 0
                session['user_data'] = {}
            else:
                emit('response', {'id': str(new_message.id), 'message': next_question["question"]})

        except Exception as e:
            app.logger.error(f"Error handling message for user {user_id}: {str(e)}")
            emit('response', {'id': '0', 'message': f"An error occurred: {str(e)}"})

        finally:
            # Ensure consistent state and logging
            if new_message:
                app.logger.info(f"Completed handling of message {new_message.id} for user {user_id}.")
            else:
                app.logger.warning(f"No message object was created during handling for user {user_id}.")
            app.logger.info(f"Final user_data state for user {user_id}: {session.get('user_data', {})}")

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handles a WebSocket client disconnection."""
        app.logger.info("Client disconnected from WebSocket")
