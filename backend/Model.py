import cohere
from rich import print
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
cohereAPIKey = env_vars.get("CohereAPIKey")

if not cohereAPIKey:
    raise ValueError("Cohere API key not found in .env file.")

co = cohere.Client(api_key=cohereAPIKey)

funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]

messages = []
preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation.
*** Do not answer any query, just decide what kind of query is given to you. ***
...
"""

ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome open firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},
    {"role": "User", "message": "what is today's date and remind me I have a dance performance on 5th Aug"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 5th Aug dance performance"},
    {"role": "User", "message": "chat with me"},
    {"role": "Chatbot", "message": "general chat with you"},
]

def FirstLayerDMM(prompt: str = 'test'):
    messages.append({"role": "User", "content": prompt})
    
    stream = co.chat_stream(
        model='command-r-plus',
        message=prompt,
        temperature=0.7,
        chat_history=ChatHistory,
        prompt_truncation='OFF',
        connectors=[],
        preamble=preamble
    )
    
    response = ""
    for event in stream:
        if event.event_type == 'text-generation':
            response += event.text
    
    response = response.replace("\n", "").split(",")
    response = [i.strip() for i in response]
    
    temp = []
    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)
    
    response = temp
    
    if '(query)' in response:
        return FirstLayerDMM(prompt=prompt)  # Recursively call if query is unclear
    else:
        return response

if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        print(FirstLayerDMM(user_input))