import openai  # type: ignore
from .models import ConversationLog

CONVERSATION_FLOW = [
    {"question": "Welcome! What is your name?", "type": "text"},
    {"question": "How old are you?", "type": "number"},
    {"question": "What is your gender?", "type": "text"},
    {"question": "What is your favorite hobby?", "type": "text"},
]

def get_next_question(conversation_stage):
    """
    Retrieve the next question in the conversation flow based on the user's stage.

    Parameters:
    -----------
    conversation_stage : int
        The current stage of the conversation (index in the flow).

    Returns:
    --------
    dict or None
        Returns the next question as a dictionary if available, otherwise None.
    """
    if conversation_stage < len(CONVERSATION_FLOW):
        return CONVERSATION_FLOW[conversation_stage]
    return None

def generate_facilitator_response(user_data):
    """
    Generate a summary based on the user's provided data.

    Parameters:
    -----------
    user_data : dict
        A dictionary containing user responses to all questions.

    Returns:
    --------
    str
        A summary message for the user based on the collected data.
    """
    name = user_data.get('name', 'unknown')
    age = user_data.get('age', 'unknown')
    gender = user_data.get('gender', 'unspecified')
    hobby = user_data.get('hobby', 'none specified')

    return f"Nice to meet you, {name}! You are {age} years old, identify as {gender}, and enjoy {hobby}."
    