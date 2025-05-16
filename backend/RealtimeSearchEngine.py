from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
import os
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")  # Default to "User" if not set
Assistance = env_vars.get("Assistantname", "Jarvis")  # Default bot name
GroqAPIKey = env_vars.get("GroqAPIKey")

# Ensure API key exists
if not GroqAPIKey:
    raise ValueError("ERROR: GroqAPIKey is missing in .env file.")

client = Groq(api_key=GroqAPIKey)

# Ensure chat log directory exists
CHAT_LOG_PATH = "Dat/ChatLog.json"
os.makedirs(os.path.dirname(CHAT_LOG_PATH), exist_ok=True)

# Load previous chat messages or create an empty list
try:
    with open(CHAT_LOG_PATH, "r") as f:
        messages = load(f)
    if not isinstance(messages, list):  # Prevents errors if JSON is malformed
        messages = []
except (FileNotFoundError, ValueError):
    messages = []
    with open(CHAT_LOG_PATH, "w") as f:
        dump(messages, f, indent=4)

# System Prompt
System = f"""Hello, I am {Username}, and you are a very accurate and advanced AI chatbot named {Assistance}.
You have real-time up-to-date information from the internet.
*** Provide answers in a professional manner, ensuring proper grammar, punctuation, and formatting. ***
*** Just answer the question from the provided data in a professional way. ***"""

# Function to perform Google Search
def GoogleSearch(query):
    try:
        results = list(search(query, num_results=5))
        answer = f"The search results for '{query}' are:\n[start]\n"
        for i, result in enumerate(results, 1):
            answer += f"{i}. {result}\n"
        answer += "[end]"
        return answer
    except Exception as e:
        return f"Error performing Google Search: {str(e)}"

# Function to clean up answer text
def AnswerModifier(answer):
    lines = answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

# Function to provide real-time information
def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime('%Y')
    time = current_date_time.strftime('%H:%M:%S')

    return (f"Use this real-time information if needed:\n"
            f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\nTime: {time}")

# Function to generate chatbot response
def ChatBotResponse(user_input):
    global messages
    messages.append({"role": "user", "content": user_input})

    # Adding real-time information
    real_time_info = Information()

    # Making a request to the Groq API
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # ✅ Updated to best available model
            messages=messages + [{"role": "system", "content": real_time_info}]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"API error: {str(e)}"

    answer = AnswerModifier(answer)
    messages.append({"role": "assistant", "content": answer})

    # Saving chat history
    with open(CHAT_LOG_PATH, "w") as f:
        dump(messages, f, indent=4)

    return answer

# Main function to run the chatbot
def main():
    print(f"{Assistance}: Hello, how can I help you?")
    while True:
        user_input = input(f"{Username}: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print(f"{Assistance}: Goodbye!")
            break
        response = ChatBotResponse(user_input)
        print(f"{Assistance}: {response}")

# Run the chatbot
if __name__ == "__main__":
    main()
