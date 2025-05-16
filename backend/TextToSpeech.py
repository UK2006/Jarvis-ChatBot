import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-IN-NeerjaNeural")  # Default voice

async def TextToAudioFile(text) -> None:
    file_path = r"Data/speech.mp3"

    # Ensure directory exists
    os.makedirs("Data", exist_ok=True)

    if os.path.exists(file_path):
        os.remove(file_path)  # Remove old file to avoid conflicts

    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)

def TTS(Text, func=lambda r=None: True):
    try:
        asyncio.run(TextToAudioFile(Text))  # Generate speech file

        pygame.mixer.init()
        pygame.mixer.music.load(r"Data/speech.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if not func():
                break
            pygame.time.Clock().tick(10)  # Corrected pygame.clock usage

        return True

    except Exception as e:
        print(f"Error in TTS: {e}")
    
    finally:
        try:
            func(False)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error in finally block: {e}")

def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")
    responses = []
    # if len(Data) > 4 and len(Text) >= 250:
    #     TTS(" ".join(Data[:2]) + ".", func)  # Fixed incorrect variable name `Test`
    # else:
    #     TTS(Text, func)

if __name__ == "__main__":
    while True:
        user_input = input("Enter the text: ")
        if user_input.lower() == "exit":
            break
        TextToSpeech(user_input)
