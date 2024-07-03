from flask import Flask, render_template, request, jsonify, send_file
import whisper
from processing import improve_and_classify_requirements, analyze_requirement
import pandas as pd
import io

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
        
        modelo = whisper.load_model("small")
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

@app.route('/analyze_requisito', methods=['POST'])
def analyze_requisito_endpoint():
    data = request.get_json()
    requirement = data['requirement']
    try:
        sintetizado = analyze_requirement(requirement)
        return jsonify({"result": "ok", "sintetizado": sintetizado})
    except Exception as e:
        return jsonify({"result": "error", "message": str(e)}), 500

@app.route('/export_to_excel', methods=['POST'])
def export_to_excel():
    try:
        data = request.json
        improved_requirements = data['improved_requirements']
        classifications = data['classifications']

        # Crear un DataFrame con todos los requisitos acumulados
        df = pd.DataFrame({
            'Requisito Mejorado': improved_requirements,
            'Clasificación': classifications
        })

        # Crear un objeto BytesIO para almacenar el archivo Excel
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Requisitos')
        writer.close()  # Usamos writer.close() en lugar de writer.save()
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name="requisitos.xlsx"
        )
    
    except Exception as e:
        print(f"Error al exportar a Excel: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
