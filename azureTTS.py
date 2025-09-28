import os
import time
import pygame
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuración: usar OPENAI_API_KEY en lugar de Azure
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # No lanzar excepción al importar; funciones lanzarán si falta la key
    OPENAI_API_KEY = None

OPENAI_TTS_URL = os.getenv("OPENAI_TTS_URL", "https://api.openai.com/v1/audio/speech")


def text_to_speech(text, filename="output.mp3", model="gpt-4o-mini-tts", voice="alloy"):
    """
    Convierte texto a un archivo MP3 usando la API de OpenAI.

    Args:
      text (str): Texto a sintetizar.
      filename (str): Ruta del archivo MP3 de salida.
      model (str): Modelo TTS a usar (por defecto 'gpt-4o-mini-tts').
      voice (str): Voz a solicitar si el endpoint la soporta.

    Returns:
      str: Ruta al archivo guardado.

    Lanza:
      ValueError si falta la clave OPENAI_API_KEY.
      requests.HTTPError si la API responde con error.
    """
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY no está configurada en las variables de entorno"
        )

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    payload = {
        "model": model,
        "voice": voice,
        "input": text,
    }

    # Hacemos la petición POST y guardamos el contenido binario en filename
    resp = requests.post(
        OPENAI_TTS_URL, headers=headers, json=payload, stream=True, timeout=30
    )
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        # Incluir cuerpo de respuesta corta en el error para debug
        msg = resp.text
        raise requests.HTTPError(f"OpenAI TTS error: {resp.status_code} - {msg}")

    # Guardar respuesta en archivo binario
    with open(filename, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return filename


def play_and_delete_audio(file_path, wait=True):
    """Reproduce un archivo de audio (MP3) con pygame y lo elimina al terminar.

    Args:
      file_path (str): Ruta del archivo MP3.
      wait (bool): Si True, bloquea hasta que termine la reproducción.
    """
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(file_path)
        audio_duration = pygame.mixer.Sound(file_path).get_length()
        pygame.mixer.music.play()
        if wait:
            time.sleep(audio_duration)
            pygame.mixer.music.stop()
    finally:
        try:
            pygame.mixer.quit()
        except Exception:
            pass
        # Eliminar el archivo si existe
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass


def speak(text, filename="output.mp3", model="gpt-4o-mini-tts", voice="alloy"):
    """Atajo: sintetiza y reproduce el texto usando OpenAI TTS.

    Devuelve la ruta del archivo MP3 temporal si se necesita.
    """
    mp3 = text_to_speech(text, filename=filename, model=model, voice=voice)
    play_and_delete_audio(mp3)


if __name__ == "__main__":
    # Prueba local mínima: no llama la API si falta la key
    sample = "Este es un test rápido de TTS con OpenAI."
    if OPENAI_API_KEY:
        print("Generando audio de prueba...")
        try:
            speak(sample)
        except Exception as e:
            print("Error al sintetizar:", e)
    else:
        print(
            "OPENAI_API_KEY no encontrada. Establece la variable de entorno para probar."
        )
