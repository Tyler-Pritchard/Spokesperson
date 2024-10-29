from flask import session, request  # type: ignore
from flask_socketio import emit  # type: ignore
from .models import ConversationLog
from . import db
from .services import get_next_question, generate_facilitator_response
import openai  # type: ignore

def register_socket_handlers(socketio, app):
    """
    Registers WebSocket event handlers for the Flask-SocketIO server.

    Parameters:
    -----------
    socketio : flask_socketio.SocketIO
        The Flask-SocketIO server instance.
    app : flask.Flask
        The Flask application instance for logging and context.
    """

    @socketio.on('connect')
    def handle_connect():
        app.logger.info("Client connected via WebSocket")
        try:
            if 'user_id' not in session:
                session['user_id'] = 1
            if 'conversation_stage' not in session:
                session['conversation_stage'] = 0

            emit('response', {'id': '0', 'message': 'Welcome! You are now connected to the server.'})
            first_question = get_next_question(session['conversation_stage'])
            emit('response', {'id': '0', 'message': first_question['question']})

        except Exception as e:
            app.logger.error(f"Error on connect: {str(e)}")
            emit('response', {'id': '0', 'message': f"An error occurred: {str(e)}"})

    @socketio.on('message')
    def handle_message(data):
        try:
            user_id = session.get('user_id', 1)
            conversation_stage = session.get('conversation_stage', 0)

            new_message = ConversationLog(user_id=user_id, message=data)
            db.session.add(new_message)
            db.session.commit()

            ai_response, next_question = generate_facilitator_response(user_id, conversation_stage)

            emit('response', {'id': str(new_message.id), 'message': ai_response})

            session['conversation_stage'] += 1
            next_question_text = next_question['question'] if next_question else "Conversation complete!"
            emit('response', {'id': str(new_message.id), 'message': next_question_text})

        except Exception as e:
            app.logger.error(f"Error handling message for user {user_id}: {str(e)}")
            emit('response', {'id': '0', 'message': f"An error occurred: {str(e)}"})

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handles a WebSocket client disconnection."""
        app.logger.info("Client disconnected from WebSocket")

def generate_openai_response(user_message):
    """
    Generates a response using OpenAI's GPT-3.5-turbo model based on the user's message.

    Parameters:
    -----------
    user_message : str
        The message content sent by the client, which will be used to generate the AI response.

    Returns:
    --------
    str
        The AI-generated response content. If an error occurs, `None` is returned.
    """
    try:
        # Construct the message history for the OpenAI API call
        messages = [{"role": "user", "content": user_message}]

        # Generate a response using OpenAI's ChatCompletion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
            n=1,
            stop=None
        )

        # Extract and return the response content
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as oe:
        app.logger.error(f"OpenAI API Error: {str(oe)}")  # type: ignore
        return None
    except Exception as e:
        app.logger.error(f"Unexpected error in OpenAI response generation: {str(e)}")  # type: ignore
        return None
