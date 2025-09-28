from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
from processing import improve_and_classify_requirements, analyze_requirement
import pandas as pd
import io

app = Flask(__name__)

# Cliente OpenAI (usa OPENAI_API_KEY desde .env)
client = OpenAI()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/audio", methods=["POST"])
def audio():
    try:
        print("Recibido un archivo de audio")

        rec = request.files.get("audio")
        rec.save("test.wav")

        # Usar la API de OpenAI para transcribir el audio
        with open("test.wav", "rb") as audio_file:
            resp = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",  # Cambia según el modelo disponible en tu cuenta
                file=audio_file,
                language="es",
            )

        transcription_text = None
        if hasattr(resp, "text"):
            transcription_text = resp.text
        elif isinstance(resp, dict) and resp.get("text"):
            transcription_text = resp.get("text")
        else:
            # Fallback: intentar leer 'transcription' o similar
            transcription_text = str(resp)

        print("Texto transcrito:", transcription_text)

        improved_requirements, classifications = improve_and_classify_requirements(
            transcription_text
        )

        print("Requisitos mejorados:", improved_requirements)
        print("Clasificaciones:", classifications)

        return jsonify(
            {
                "transcription": transcription_text,
                "improved_requirements": improved_requirements,
                "classifications": classifications,
            }
        )

    except Exception as e:
        print(f"Error procesando el audio: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/analyze_requisito", methods=["POST"])
def analyze_requisito_endpoint():
    data = request.get_json()
    requirement = data["requirement"]
    try:
        sintetizado = analyze_requirement(requirement)
        return jsonify({"result": "ok", "sintetizado": sintetizado})
    except Exception as e:
        return jsonify({"result": "error", "message": str(e)}), 500


@app.route("/export_to_excel", methods=["POST"])
def export_to_excel():
    try:
        data = request.json
        improved_requirements = data["improved_requirements"]
        classifications = data["classifications"]

        df = pd.DataFrame(
            {
                "Requisito Mejorado": improved_requirements,
                "Clasificación": classifications,
            }
        )

        output = io.BytesIO()
        df.to_excel(
            output, index=False, sheet_name="Requisitos"
        )  # Usamos df.to_excel directamente con el objeto BytesIO

        output.seek(0)

        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="requisitos.xlsx",  # Nombre del archivo adjunto que se enviará
        )

    except Exception as e:
        print(f"Error al exportar a Excel: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=False)
