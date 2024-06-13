from flask import Flask, render_template, request, jsonify
import whisper
from classification import *
from modules.talk import Talk

app = Flask(__name__)

# Configuración de FakeYou
FAKEYOU_USERNAME = 
FAKEYOU_PASSWORD = 
MODEL_NAME = 'auronplay'

# Inicializar la clase Talk
talker = Talk(FAKEYOU_USERNAME, FAKEYOU_PASSWORD, MODEL_NAME)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/audio", methods=["POST"])
def audio():    
    try:
        rec = request.files.get("audio")
        rec.save("test.wav")
        modelo = whisper.load_model("small")
        file_path = "test.wav"
        transcription = modelo.transcribe(file_path, language="es")
        type_r = classify(transcription['text'])

        # Hablar el texto transcrito usando FakeYou
        talker.talk(transcription['text'])


        return {"result": "ok", "text": transcription['text'], "type": type_r}
    except Exception as e:
        print(e)
        return {"resultado": "error", "message": str(e)}

if __name__ == '__main__':
    app.run(debug=True)

    
