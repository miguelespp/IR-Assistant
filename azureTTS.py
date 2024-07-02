import os
import time
import pygame
import requests

from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig

# Configurar Azure TextToSpeech
subscription_key = ""
region = ""

# Inicializar configuración de Azure TTS
speech_config = SpeechConfig(subscription=subscription_key, region=region)

def text_to_speech(text):
    # Utilizar el sintetizador de Azure TTS para convertir el texto a voz y guardarlo en "output.mp3"
    #audio_config = AudioConfig(filename="output.mp3")
    speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)
    speech_synthesizer.speak_text_async(text).get()

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