from flask import Flask, render_template, request, jsonify
import whisper
from processing import improve_and_classify_requirements, improve_requirement, sintetizar_requisito

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/audio", methods=["POST"])
def audio():
    try:
        print("Recibido un archivo de audio")  

        rec = request.files.get("audio")
        rec.save("test.wav")
        
        modelo = whisper.load_model("medium")
        file_path = "test.wav"
        transcription = modelo.transcribe(file_path, language="es")
        
        print("Texto transcrito:", transcription['text'])
        
        improved_requirements, classifications = improve_and_classify_requirements(transcription['text'])
        
        print("Requisitos mejorados:", improved_requirements)
        print("Clasificaciones:", classifications)
        
        return jsonify({
            "transcription": transcription['text'],
            "improved_requirements": improved_requirements,
            "classifications": classifications
        })
    
    except Exception as e:
        print(f"Error procesando el audio: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/mejorar_requisito', methods=['POST'])
def mejorar_requisito():
    data = request.get_json()
    requirement = data.get('requirement')
    classification = data.get('classification')

    if not requirement:
        return jsonify({"result": "error", "message": "No se proporcionó un requisito"}), 400

    improved_requirement = improve_requirement(requirement, classification)
    return jsonify({"result": "ok", "improved_requirement": improved_requirement})

@app.route('/sintetizar_requisito', methods=['POST'])
def sintetizar_requisito_endpoint():
    data = request.get_json()
    requirement = data['requirement']
    try:
        sintetizado = sintetizar_requisito(requirement)
        return jsonify({"result": "ok", "sintetizado": sintetizado})
    except Exception as e:
        return jsonify({"result": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
