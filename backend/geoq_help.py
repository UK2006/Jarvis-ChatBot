from groq import Groq
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API Key from .env
GroqAPIKey = os.getenv("GroqAPIKey")

# Ensure API key exists
if not GroqAPIKey:
    print("ERROR: GroqAPIKey is missing. Please check your .env file.")
    exit()

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

try:
    # Fetch available models
    response = client.models.list()

    # Check response type
    if not hasattr(response, "data"):
        print(f"❌ Unexpected response format: {response}")
        exit()

    models = response.data  # Correct way to access models

    # Print available models
    print("✅ Available Groq Models:")
    for model in models:
        print(f"- {model.id}")

except Exception as e:
    print(f"❌ API error: {e}")
