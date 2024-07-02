import requests
import json
import pygame
import os
import time

# Define constants for the script
CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
XI_API_KEY = "<xi-api-key>"  # Your API key for authentication
VOICE_ID = "<voice-id>"  # ID of the voice model to use
OUTPUT_PATH = "output.mp3"  # Path to save the output audio file

# Function to convert text to speech using Eleven Labs API
def text_to_speech(text, output_path=OUTPUT_PATH):
    tts_url = "https://api.elevenlabs.io/v1/text-to-speech/usMX8xBSRinaTzC4cdpz"
    
    headers = {
        "Accept": "application/json",
        "xi-api-key": "sk_76393875e66dde805f70eaf373268aaba7ffed9457cb1391"
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }
    
    response = requests.post(tts_url, headers=headers, json=data, stream=True)
    
    if response.ok:
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        print("Audio stream saved successfully.")
    else:
        print(response.text)

# Function to play the audio file and delete it afterwards
def play_and_delete_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    audio_duration = pygame.mixer.Sound(file_path).get_length()
    pygame.mixer.music.play()
    time.sleep(audio_duration)
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove(file_path)