from flask_sqlalchemy import SQLAlchemy # type: ignore

# Initialize the database object
db = SQLAlchemy()

# User model for storing profiles
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

# Conversation Log model for storing user responses
class ConversationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    # Define a relationship between User and ConversationLog
    user = db.relationship('User', backref=db.backref('conversations', lazy=True))
