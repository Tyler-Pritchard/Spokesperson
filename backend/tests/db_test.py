# db_test.py
from app import app, db, User, ConversationLog  # Import app and db from your main application

# Start the app context
with app.app_context():
    # Add a test user
    test_user = User(username="TestUserDB")
    db.session.add(test_user)
    db.session.commit()
    print(f"Test user {test_user.username} added successfully with ID: {test_user.id}")

    # Add a test conversation
    test_message = ConversationLog(user_id=test_user.id, message="Hello, this is a test message!")
    db.session.add(test_message)
    db.session.commit()
    print(f"Test message added successfully with ID: {test_message.id}")

    # Query the database
    users = User.query.all()
    print(f"Users in the database: {users}")

    messages = ConversationLog.query.all()
    print(f"Messages in the database: {messages}")
