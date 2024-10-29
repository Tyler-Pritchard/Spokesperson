import openai  # type: ignore
from .models import ConversationLog

def generate_facilitator_response(user_id, conversation_stage):
    """
    Generate a response from OpenAI based on the conversation history and conversation stage.

    Parameters:
    -----------
    user_id : int
        The ID of the user.
    conversation_stage : int
        The stage of the conversation to select the appropriate response or question.

    Returns:
    --------
    tuple : (str, dict or None)
        Returns the AI-generated response and the next question (or None if no more questions).
    """
    try:
        # Retrieve previous conversation logs
        conversation_logs = ConversationLog.query.filter_by(user_id=user_id).order_by(ConversationLog.timestamp).all()

        if not conversation_logs:
            return "No conversation history found for this user.", get_next_question(conversation_stage)

        conversation_text = "\n".join([f"User: {log.message}" for log in conversation_logs])

        messages = [
            {"role": "system", "content": "You are a helpful AI that guides the user through questions to build a profile."},
            {"role": "user", "content": conversation_text}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            n=1
        )

        ai_response = response['choices'][0]['message']['content'].strip()

        # Get the next question
        next_question = get_next_question(conversation_stage + 1)
        return ai_response, next_question

    except Exception as e:
        return f"An error occurred: {str(e)}", None


CONVERSATION_FLOW = [
    {"question": "What is your name?", "type": "text"},
    {"question": "How old are you?", "type": "number"},
    {"question": "What is your favorite hobby?", "type": "text"},
    {"question": "Do you prefer mountains or the beach?", "type": "choice", "options": ["Mountains", "Beach"]},
    # Add more questions as needed
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
        Returns the next question as a dictionary if available, otherwise returns a message
        indicating the end of the conversation.
    """
    if conversation_stage < len(CONVERSATION_FLOW):
        return CONVERSATION_FLOW[conversation_stage]
    return {"question": "Thank you! This concludes the conversation.", "type": "end"}