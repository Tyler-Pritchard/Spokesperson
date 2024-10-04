# db_test.py
"""
Database testing script for the Spokesperson application.
This script creates a test user and a test conversation log entry,
then queries and prints the database contents for verification.
"""

import sys
import os
from sqlalchemy.exc import IntegrityError # type: ignore

if os.path.exists('spokesperson.db'):
    os.remove('spokesperson.db')

# Ensure that the application modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db  # Import the app factory and db instance
from app.models import User, ConversationLog  # Import models for database operations

# Create the Flask application using the factory function
app, _, _ = create_app()  # Ignore socketio and db in the tuple return values for this test

# Use the application context to perform database operations
with app.app_context():
    # Check if the test user already exists to avoid duplicate entries
    existing_user = User.query.filter_by(username="TestUserDB").first()

    if not existing_user:
        # Create a test user and add to the database
        test_user = User(username="TestUserDB")
        db.session.add(test_user)
        try:
            db.session.commit()
            print(f"Test user '{test_user.username}' added successfully with ID: {test_user.id}")
        except IntegrityError:
            db.session.rollback()
            print("Error: User with username 'TestUserDB' already exists in the database.")
            test_user = User.query.filter_by(username="TestUserDB").first()
    else:
        print(f"User '{existing_user.username}' already exists with ID: {existing_user.id}")
        test_user = existing_user

    # Check if the test message already exists
    existing_message = ConversationLog.query.filter_by(user_id=test_user.id, message="Hello, this is a test message!").first()

    if not existing_message:
        # Create a test conversation log entry associated with the test user
        test_message = ConversationLog(user_id=test_user.id, message="Hello, this is a test message!")
        db.session.add(test_message)
        db.session.commit()
        print(f"Test message added successfully with ID: {test_message.id}")
    else:
        print(f"Message already exists: ID {existing_message.id}, User ID: {existing_message.user_id}")

    # Query and display all users in the database
    users = User.query.all()
    print("Users in the database:")
    for user in users:
        print(f" - {user.username} (ID: {user.id})")

    # Query and display all conversation logs in the database
    messages = ConversationLog.query.all()
    print("Messages in the database:")
    for message in messages:
        print(f" - User ID: {message.user_id}, Message: '{message.message}', Timestamp: {message.timestamp}")
