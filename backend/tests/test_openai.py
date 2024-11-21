import openai  # type: ignore # Import OpenAI's Python package for API interaction
import os
from dotenv import load_dotenv  # type: ignore # Import to load environment variables from .env
from openai.error import OpenAIError  # type: ignore # Import OpenAIError for better error handling

# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure the API key is loaded

def test_openai_api():
    """
    Test the OpenAI API by sending a sample request to the GPT-3.5-turbo model.
    This function queries the model with a simple user prompt and returns the response.
    """
    try:
        # Construct the message for the OpenAI model
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]
        
        # Make the API call to OpenAI's ChatCompletion endpoint
        response = openai.ChatCompletion.create(
            model="o1-preview",  # Model specification
            messages=messages,  # User and system input
            max_tokens=50  # Limit the response length
        )
        
        # Extract and print the AI response
        ai_response = response['choices'][0]['message']['content'].strip()
        print(f"AI Response: {ai_response}")

    except OpenAIError as e:
        # Handle specific OpenAI API errors
        print(f"❌ OpenAI API Error: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    # Run the OpenAI test
    test_openai_api()
