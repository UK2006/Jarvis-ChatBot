import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# Ensure Data folder exists
os.makedirs("Data", exist_ok=True)

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    """Sends request to API and returns image bytes"""
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.content
    else:
        print(f"API Error: {response.status_code}, {response.text}")
        return None

async def generate_images(prompt: str):
    """Generates 4 images using Hugging Face API"""
    tasks = []
    for i in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        filename = fr"Data\{prompt.replace(' ', '_')}{i + 1}.jpg"

        if image_bytes:  # Ensure we got valid data
            with open(filename, "wb") as f:
                f.write(image_bytes)
            print(f"✅ Image saved: {filename}")  # Debugging
        else:
            print(f"❌ Failed to generate image: {filename}")

def open_images(prompt):
    """Opens generated images"""
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        if os.path.exists(image_path):  # Check if file exists before opening
            try:
                img = Image.open(image_path)
                print(f"🖼️ Opening image: {image_path}")
                img.show()
                sleep(1)
            except IOError:
                print(f"❌ Error opening {image_path}")
        else:
            print(f"⚠️ File not found: {image_path}")  # Debugging

def GenerateImages(prompt: str):
    """Runs image generation and opens them"""
    asyncio.run(generate_images(prompt))
    open_images(prompt)

while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", 'r') as f:
            Data: str = f.read()

        Prompt, Status = Data.split(',')
        if Status.strip().lower() == "true":
            print("🎨 Generating Images...")
            GenerateImages(prompt=Prompt)

            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            break
        else:
            sleep(1)
    except Exception as e:
        print(f"❌ Error: {e}")
