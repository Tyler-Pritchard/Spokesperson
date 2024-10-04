import openai # type: ignore
import os
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

# Load environment variables or set OpenAI API key directly
openai.api_key = os.getenv("OPENAI_API_KEY") 

# Retrieve the list of available engines/models
try:
    engines = openai.Engine.list()
    print("Available Engines/Models:")
    for engine in engines['data']:
        print(f"ID: {engine['id']}, Object: {engine['object']}")
except Exception as e:
    print(f"Error retrieving engines: {e}")
