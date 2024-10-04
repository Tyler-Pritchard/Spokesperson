import openai  # type: ignore
from .models import ConversationLog

def generate_facilitator_response(user_id):
    """
    Generate a response from OpenAI based on previous conversation logs for the specified user.

    Parameters:
    -----------
    user_id : int
        The ID of the user whose conversation logs will be used to generate a response.

    Returns:
    --------
    str
        The AI-generated response from OpenAI, based on the user's conversation history.
        If an error occurs during the generation, the error message is returned instead.

    Example Usage:
    --------------
    response = generate_facilitator_response(user_id=1)
    print(response)

    Note:
    -----
    This function uses the OpenAI ChatCompletion API (gpt-3.5-turbo) to generate
    responses. Ensure that your OpenAI API key is correctly set in the environment variables.
    """
    try:
        # Retrieve previous conversation logs for the specified user, sorted by timestamp
        conversation_logs = ConversationLog.query.filter_by(user_id=user_id).order_by(ConversationLog.timestamp).all()
        
        if not conversation_logs:
            return "No conversation history found for this user."

        # Format conversation logs into a single string for use as the input prompt
        conversation_text = "\n".join([f"User: {log.message}" for log in conversation_logs])

        # Construct the message history for the OpenAI API call
        messages = [
            {"role": "system", "content": "You are a helpful AI Facilitator guiding a user to build a personalized chatbot profile."},
            {"role": "user", "content": conversation_text}
        ]

        # Generate a response using OpenAI's ChatCompletion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,  # Adjust the maximum token count as needed
            n=1,             # Generate only a single response
            stop=None        # Optionally, you can specify stop sequences if needed
        )

        # Extract and return the AI-generated response content
        ai_response = response['choices'][0]['message']['content'].strip()
        return ai_response

    except openai.error.OpenAIError as oe:
        # Return OpenAI-specific errors for better debugging
        return f"OpenAI API Error: {str(oe)}"
    except Exception as e:
        # Return generic errors
        return f"An unexpected error occurred: {str(e)}"
