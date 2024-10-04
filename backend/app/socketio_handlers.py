from flask import session # type: ignore
from flask_socketio import emit # type: ignore
from .models import ConversationLog
from . import db
import openai # type: ignore

def register_socket_handlers(socketio, app):
    """Registers all the WebSocket event handlers."""
    
    @socketio.on('connect')
    def handle_connect():
        app.logger.info("Client connected via WebSocket")
        if 'user_id' not in session:
            session['user_id'] = 1  # For testing purposes

        emit('response', {'id':'0', 'message': 'Welcome! You are now connected to the server.'})
    
    @socketio.on('message')
    def handle_message(data):
        user_id = session.get('user_id', 1)
        new_message = ConversationLog(user_id=user_id, message=data)
        db.session.add(new_message)
        db.session.commit()

        # OpenAI call
        messages = [{"role": "user", "content": data}]
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=100)
        ai_response = response['choices'][0]['message']['content'].strip()

        emit('response', {'id': str(new_message.id), 'message': ai_response}, broadcast=True)

    @socketio.on('disconnect')
    def handle_disconnect():
        app.logger.info("Client disconnected from WebSocket")
