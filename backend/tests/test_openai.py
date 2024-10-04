import openai # type: ignore
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

# Load environment variables or set OpenAI API key directly
openai.api_key = os.getenv("OPENAI_API_KEY") 

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # Specify the correct model here
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ],
    max_tokens=50
)

# Extract and print the response
print(f"AI Response: {response['choices'][0]['message']['content']}")