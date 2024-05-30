from flask import Flask, render_template, request, jsonify
import whisper
from classification import *

app = Flask(__name__)


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
        return {"result": "ok", "text": transcription['text'], "type": type_r}
    except Exception as e:
        print(e)
        return {"resultado": "error", "message": str(e)}


if __name__ == '__main__':
    app.run(debug=True)
