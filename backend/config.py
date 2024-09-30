import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for Flask application settings."""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = os.getenv("FLASK_ENV") == "development"

    @staticmethod
    def init_app(app):
        """Initialize Flask app with configuration settings."""
        app.config.from_object(Config)
