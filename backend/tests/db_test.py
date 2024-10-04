# db_test.py

from app import app, db, User, ConversationLog  # Import the app, db, and models from the main application
from sqlalchemy.exc import SQLAlchemyError

def run_db_tests():
    """
    Run a series of basic database operations to test the integration of the User and ConversationLog models.

    This script will:
    1. Start the Flask app context.
    2. Create a test user and add them to the database.
    3. Create a test conversation log and link it to the test user.
    4. Query and display all users and messages stored in the database.
    """
    try:
        with app.app_context():  # Start the application context
            # Step 1: Add a test user to the database
            test_user = User(username="TestUserDB")
            db.session.add(test_user)
            db.session.commit()
            print(f"✅ Test user '{test_user.username}' added successfully with ID: {test_user.id}")

            # Step 2: Add a test conversation message for the user
            test_message = ConversationLog(
                user_id=test_user.id,
                message="Hello, this is a test message!"
            )
            db.session.add(test_message)
            db.session.commit()
            print(f"✅ Test message added successfully with ID: {test_message.id}")

            # Step 3: Query and display all users in the database
            users = User.query.all()
            print(f"\nUsers in the database ({len(users)} total):")
            for user in users:
                print(f" - ID: {user.id}, Username: {user.username}, Created At: {user.created_at}")

            # Step 4: Query and display all conversation messages in the database
            messages = ConversationLog.query.all()
            print(f"\nMessages in the database ({len(messages)} total):")
            for message in messages:
                print(f" - ID: {message.id}, User ID: {message.user_id}, Message: {message.message}, Timestamp: {message.timestamp}")

    except SQLAlchemyError as sqle:
        print(f"❌ SQLAlchemy Error: {str(sqle)}")
        db.session.rollback()  # Rollback the transaction in case of an error
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")


if __name__ == "__main__":
    run_db_tests()
