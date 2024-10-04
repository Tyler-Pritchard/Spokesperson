import os
from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_socketio import SocketIO # type: ignore
from flask_session import Session
from flask_cors import CORS # type: ignore
from flask_limiter import Limiter # type: ignore
from flask_limiter.util import get_remote_address # type: ignore
from dotenv import load_dotenv # type: ignore
from config.config import Config

# Load environment variables
load_dotenv()

# Set up Flask extensions
db = SQLAlchemy()
socketio = SocketIO()
session = Session()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    """Application factory to create a Flask app."""
    app = Flask(__name__)

    # Load configuration settings
    app.config.from_object(Config)

    # Initialize Flask extensions
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    session.init_app(app)
    CORS(app)
    limiter.init_app(app)

    # Import blueprints and register routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Register SocketIO handlers
    from .socketio_handlers import register_socket_handlers
    register_socket_handlers(socketio, app)

    return app, socketio, db
