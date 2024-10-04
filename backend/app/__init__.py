import os

from dotenv import load_dotenv  # type: ignore # Load environment variables
from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_socketio import SocketIO # type: ignore
from flask_session import Session
from flask_cors import CORS # type: ignore
from flask_limiter import Limiter # type: ignore
from flask_limiter.util import get_remote_address # type: ignore

from config.config import Config

# Load environment variables from the .env file
load_dotenv()

# Initialize Flask extensions without an app context
db = SQLAlchemy()  # SQLAlchemy database instance
socketio = SocketIO()  # Flask-SocketIO instance for real-time WebSocket support
session = Session()  # Flask session for managing user sessions
limiter = Limiter(key_func=get_remote_address)  # Rate limiter for API request control


def create_app() -> tuple[Flask, SocketIO, SQLAlchemy]:
    """
    Application factory pattern to create and configure the Flask app instance.

    Returns:
        tuple: A tuple containing the Flask app, SocketIO instance, and SQLAlchemy instance.
    """
    # Initialize the Flask application
    app = Flask(__name__)

    # Load configuration settings from config.py
    app.config.from_object(Config)

    # Initialize Flask extensions with the app context
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    session.init_app(app)
    CORS(app)  # Enable Cross-Origin Resource Sharing
    limiter.init_app(app)

    # Import and register blueprints for routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Register SocketIO event handlers
    from .socketio_handlers import register_socket_handlers
    register_socket_handlers(socketio, app)

    return app, socketio, db


