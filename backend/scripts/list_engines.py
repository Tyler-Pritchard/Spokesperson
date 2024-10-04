import openai  # type: ignore
import os
from dotenv import load_dotenv  # type: ignore

# Load environment variables from the .env file
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def list_openai_engines():
    """
    Retrieve and print a list of available OpenAI engines/models.

    This function interacts with the OpenAI API to get a list of all available engines or models
    associated with the provided API key. The function will print the engine ID and object type
    for each available model.

    Example Output:
    ---------------
    Available Engines/Models:
    ID: text-davinci-003, Object: engine
    ID: text-curie-001, Object: engine

    Raises:
    -------
    Exception
        If an error occurs during the API call, the exception is caught and a descriptive
        message is printed to the console.
    """
    try:
        # Retrieve the list of available engines/models using the OpenAI API
        engines = openai.Engine.list()
        print("Available Engines/Models:")

        # Loop through the returned engines and print the details
        for engine in engines['data']:
            print(f"ID: {engine['id']}, Object: {engine['object']}")

    except openai.error.AuthenticationError:
        print("Error: Invalid API key provided. Please check your OpenAI API key.")
    except openai.error.OpenAIError as oe:
        print(f"OpenAI API Error: {str(oe)}. Check your API key and network connection.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    # Ensure the OpenAI API key is set before proceeding
    if openai.api_key:
        list_openai_engines()
    else:
        print("Error: OpenAI API key not set. Please configure it in your environment variables.")
