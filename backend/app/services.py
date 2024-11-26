import openai  # type: ignore
from .models import ConversationLog

CONVERSATION_FLOW = [
    {"question": "What is your name?", "type": "text", "key": "name"},
    {"question": "How old are you?", "type": "number", "key": "age"},
    {"question": "What is your gender?", "type": "text", "key": "gender"},
    {"question": "What is your favorite hobby?", "type": "text", "key": "hobby"},
    {"question": "Would you describe yourself as more adventurous or more routine-oriented?", "type": "choice", "key": "personality", "options": ["Adventurous", "Routine-oriented"]},
    {"question": "What kind of conversations do you enjoy? Banter or deep discussions?", "type": "choice", "key": "communication", "options": ["Banter", "Deep discussions"]},
    {"question": "What’s something you’re passionate about?", "type": "text", "key": "passion"},
    {"question": "Describe your ideal date. What does it look like?", "type": "text", "key": "ideal_date"}
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
    name = user_data.get("name", "User")
    age = user_data.get("age", "unknown")
    gender = user_data.get("gender", "not specified")
    hobby = user_data.get("hobby", "no particular hobby")
    personality = user_data.get("personality", "no preference")
    communication = user_data.get("communication", "not specified")
    passion = user_data.get("passion", "no specific passion shared")
    ideal_date = user_data.get("ideal_date", "not described")

    summary_message = (
        f"Nice to meet you, {name}! You are {age} years old, identify as {gender}, "
        f"and enjoy {hobby}. You see yourself as {personality} and prefer {communication}. "
        f"You are passionate about {passion}, and your ideal date involves {ideal_date}."
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
    
    
def validate_input(input_value, input_type, options=None):
    """
    Validate the user input based on the expected input type.

    Parameters:
    -----------
    input_value : str
        The input provided by the user.
    input_type : str
        The expected type of the input (e.g., text, number, choice).
    options : list, optional
        Valid options for 'choice' type inputs.

    Returns:
    --------
    bool
        True if input is valid, False otherwise.
    """
    try:
        if input_type == "text":
            return bool(input_value.strip())
        elif input_type == "number":
            return input_value.isdigit() and int(input_value) > 0
        elif input_type == "choice":
            return input_value in options if options else False
        else:
            return False
    except Exception:
        return False
