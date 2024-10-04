from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column # type: ignore
from sqlalchemy import ForeignKey, String, Integer, DateTime # type: ignore
from . import db

class User(db.Model):
    """
    User model represents a registered user in the system.

    Attributes:
    -----------
    id : int
        Unique identifier for the user.
    username : str
        Username of the user, must be unique.
    created_at : datetime
        Timestamp of when the user was created.
    """
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Primary key
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)  # Unique username
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)  # Account creation timestamp
    
    # Relationship to ConversationLog model
    conversations: Mapped[list['ConversationLog']] = relationship('ConversationLog', back_populates='user')


class ConversationLog(db.Model):
    """
    ConversationLog model stores individual chat messages for each user.

    Attributes:
    -----------
    id : int
        Unique identifier for each message.
    user_id : int
        Foreign key to associate the message with a user.
    message : str
        The content of the message.
    timestamp : datetime
        Timestamp of when the message was sent.
    """
    __tablename__ = 'conversation_log'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Primary key
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)  # Foreign key to User model
    message: Mapped[str] = mapped_column(String, nullable=False)  # Message content
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)  # Message timestamp

    # Establish the relationship to the User model
    user: Mapped[User] = relationship('User', back_populates='conversations')
