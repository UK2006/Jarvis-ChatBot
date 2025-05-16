from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# User agent for web scraping
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize Groq API client
client = Groq(api_key=GroqAPIKey)

# Default system prompt for chatbot
SystemChatBot = [
    {"role": "system", "content": f"Hello, I am {os.environ.get('Username', 'AI Assistant')}. You're a content writer. You have to write content like a letter."}
]

# Placeholder for chatbot messages
messages = []

def GoogleSearch(Topic):
    """Searches the topic on Google."""
    search(Topic)
    return True

def OpenNotepad(File):
    """Opens a given file in Notepad."""
    default_text_editor = 'notepad.exe'
    subprocess.Popen([default_text_editor, File])

def ContentWriterAI(prompt):
    """Generates content using Groq AI API based on a given prompt."""
    messages.append({"role": "user", "content": prompt})
    
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=SystemChatBot + messages,
        max_tokens=2048,
        temperature=0.7,
        top_p=1,
        stream=True,  # Fixed typo
        stop=None
    )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.replace("</s", "")
    messages.append({"role": "assistant", "content": Answer})

    return Answer

def Content(Topic):
    """Writes content based on the given topic and opens it in Notepad."""
    Topic = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)
    
    # Ensure directory exists
    os.makedirs("Data", exist_ok=True)

    file_path = rf"Data\{Topic.lower().replace(' ', '_')}.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    OpenNotepad(file_path)
    return True

def YouTubeSearch(Topic):
    """Searches a topic on YouTube."""
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    """Plays a YouTube video."""
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    """Attempts to open an application. If not found, searches for an online alternative."""
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f'https://www.google.com/search?q={query}'
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search results.")
                return None

        html = search_google(app)
        if html:
            links = extract_links(html)
            if links:
                webopen(links[0])
        return True

def CloseApp(app):
    """Closes an application, except for Chrome."""
    if "chrome" in app:
        return False
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

def System(command):
    """Controls system volume settings."""
    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True

async def TranslateAndExecute(commands: list[str]):
    """Executes a list of commands asynchronously."""
    funcs = []
    for command in commands:
        if command.startswith("open"):
            if "open it" in command:
                pass
            elif "open file" in command:
                pass
            else:
                funcs.append(lambda: OpenApp(command.replace("open ", "")))

        elif command.startswith("search"):
            topic = command.replace("search ", "")
            funcs.append(lambda: GoogleSearch(topic))

        elif command.startswith("play on youtube"):
            query = command.replace("play on youtube ", "")
            funcs.append(lambda: PlayYoutube(query))

        elif command.startswith("content"):
            topic = command.replace("content ", "")
            funcs.append(lambda: Content(topic))

        elif command.startswith("close"):
            app_name = command.replace("close ", "")
            funcs.append(lambda: CloseApp(app_name))

        elif command in ["mute", "unmute", "volume up", "volume down"]:
            funcs.append(lambda: System(command))

    for func in funcs:
        await asyncio.to_thread(func)

if __name__ == "__main__":
    while True:
        user_input = input("Enter a command (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        asyncio.run(TranslateAndExecute([user_input]))
