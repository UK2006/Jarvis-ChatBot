from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")  # Default to "User" if not found
Assistance = env_vars.get("Assistantname", "Assistant")  # Default if not found
GrooqAPIKey = env_vars.get("GroqAPIKey")  # Match exactly with .env file
  # Load API key

# Check if API key is missing
if not GrooqAPIKey:
    raise ValueError("Error: GROQ_API_KEY is missing. Please check your .env file.")

# Initialize Groq client
client = Groq(api_key=GrooqAPIKey)

# Chat history initialization
messages = []
System = f"""Hello, I am {Username}. You are a very accurate and advanced AI chatbot named {Assistance}, which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [{"role": "system", "content": System}]

# Load previous chat history if exists
try:
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open("Data/ChatLog.json", "w") as f:
        dump([], f)

# Function to provide real-time information
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    return f"Current Date and Time: {current_date_time.strftime('%A, %d %B %Y %H:%M:%S')}"

# ChatBot function
def ChatBot(Query):
    try:
        # Load chat history
        with open("Data/ChatLog.json", "r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": Query})

        # Call Groq API
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=False  # Change to False to avoid issues
        )

        Answer = completion.choices[0].message.content

        messages.append({"role": "assistant", "content": Answer})

        # Save chat history
        with open("Data/ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return Answer
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred. Please try again."

# Main Loop
if __name__ == '__main__':
    while True:
        user_input = input("Enter your question: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        print(ChatBot(user_input))
