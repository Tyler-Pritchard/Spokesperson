import openai  # type: ignore
from .models import ConversationLog

CONVERSATION_FLOW = [
    {"question": "What is your name?", "type": "text", "key": "name"},
    {"question": "How old are you?", "type": "number", "key": "age"},
    {"question": "What is your gender?", "type": "text", "key": "gender"},
    {"question": "What is your favorite hobby?", "type": "text", "key": "hobby"}
]

def get_next_question(conversation_stage, user_data):
    """
    Retrieve the next question or summary at the end of the conversation.

    Parameters:
    -----------
    conversation_stage : int
        The current stage of the conversation (index in the flow).
    user_data : dict
        Dictionary containing the user's collected responses.

    Returns:
    --------
    dict
        The next question or a summary message.
    """
    if conversation_stage < len(CONVERSATION_FLOW):
        return CONVERSATION_FLOW[conversation_stage]
    
    # If conversation_stage exceeds the flow, provide a summary message.
    name = user_data.get('name', 'there')
    age = user_data.get('age', 'unknown age')
    gender = user_data.get('gender', 'not specified')
    hobby = user_data.get('hobby', 'no hobbies listed')

    summary_message = (
        f"Nice to meet you, {name}! You are {age} years old, identify as {gender}, and enjoy {hobby}."
    )
    return {"question": summary_message, "type": "end"}



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
    name = user_data.get("name", "User")
    age = user_data.get("age", "unknown")
    gender = user_data.get("gender", "not specified")
    hobby = user_data.get("hobby", "no particular hobby")

    return f"Nice to meet you, {name}! You are {age} years old, identify as {gender}, and enjoy {hobby}."
    