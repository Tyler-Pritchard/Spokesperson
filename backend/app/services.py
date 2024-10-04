import openai # type: ignore
from .models import ConversationLog

def generate_facilitator_response(user_id):
    """Generate a response from OpenAI based on previous conversation logs."""
    try:
        conversation_logs = ConversationLog.query.filter_by(user_id=user_id).all()
        conversation_text = "\n".join([f"User: {log.message}" for log in conversation_logs])

        messages = [
            {"role": "system", "content": "You are a helpful AI."},
            {"role": "user", "content": conversation_text}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            n=1
        )

        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return str(e)
