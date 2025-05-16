from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import time

# Load environment variables
env_vars = dotenv_values('.env')
InputLanguage = env_vars.get("InputLanguage", "en")  # Default to English if not set

# Define HTML content
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            if (recognition) {
                recognition.stop();
                output.innerHTML = "";
            }
        }
    </script>
</body>
</html>'''

# Modify HTML with selected input language
HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Save HTML file
html_file_path = os.path.join(os.getcwd(), "Data", "Voice.html")
os.makedirs(os.path.dirname(html_file_path), exist_ok=True)

with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Set up Selenium WebDriver
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.37"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--use-fake-ui-for-media-stream')
chrome_options.add_argument('--use-fake-device-for-media-stream')
chrome_options.add_argument('--headless=new')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Paths
TempDirPath = os.path.join(os.getcwd(), 'Frontend', 'Files')

# Helper function to set assistant status
def SetAssistantStatus(Status):
    os.makedirs(TempDirPath, exist_ok=True)
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding="utf-8") as file:
        file.write(Status)

# Function to modify query
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "how's"]

    if any(new_query.startswith(word + " ") for word in question_words):
        new_query = new_query.rstrip('.?!') + "?"
    else:
        new_query = new_query.rstrip('.?!') + "."

    return new_query.capitalize()

# Function to translate text
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Function to handle speech recognition
def SpeechRecognition():
    driver.get("file://" + html_file_path)
    driver.find_element(By.ID, "start").click()
    
    while True:
        try:
            Text = driver.find_element(By.ID, "output").text
            if Text:
                driver.find_element(By.ID, "end").click()
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception:
            time.sleep(1)  # Prevent excessive looping

# Main loop
if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        print(Text)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import time

# Load environment variables
env_vars = dotenv_values('.env')
InputLanguage = env_vars.get("InputLanguage", "en")  # Default to English if not set

# Define HTML content
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            if (recognition) {
                recognition.stop();
                output.innerHTML = "";
            }
        }
    </script>
</body>
</html>'''

# Modify HTML with selected input language
HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Save HTML file
html_file_path = os.path.join(os.getcwd(), "Data", "Voice.html")
os.makedirs(os.path.dirname(html_file_path), exist_ok=True)

with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Set up Selenium WebDriver
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.37"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--use-fake-ui-for-media-stream')
chrome_options.add_argument('--use-fake-device-for-media-stream')
chrome_options.add_argument('--headless=new')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Paths
TempDirPath = os.path.join(os.getcwd(), 'Frontend', 'Files')

# Helper function to set assistant status
def SetAssistantStatus(Status):
    os.makedirs(TempDirPath, exist_ok=True)
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding="utf-8") as file:
        file.write(Status)

# Function to modify query
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "how's"]

    if any(new_query.startswith(word + " ") for word in question_words):
        new_query = new_query.rstrip('.?!') + "?"
    else:
        new_query = new_query.rstrip('.?!') + "."

    return new_query.capitalize()

# Function to translate text
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Function to handle speech recognition
def SpeechRecognition():
    driver.get("file://" + html_file_path)
    driver.find_element(By.ID, "start").click()
    
    while True:
        try:
            Text = driver.find_element(By.ID, "output").text
            if Text:
                driver.find_element(By.ID, "end").click()
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception:
            time.sleep(1)  # Prevent excessive looping

# Main loop
if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        print(Text)
