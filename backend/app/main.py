from app import create_app
from flask import Flask # type: ignore
from flask_socketio import SocketIO # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

# Create the Flask app and initialize extensions (SocketIO and SQLAlchemy)
app: Flask
socketio: SocketIO
db: SQLAlchemy
app, socketio, db = create_app()

if __name__ == '__main__':
    # Run the Flask-SocketIO app on the specified host and port in debug mode
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
