# CHANGELOG

Todas las modificaciones importantes del proyecto se registran aquí.

## [Unreleased] - 2025-09-27
### Agregado
- Implementación de TTS centralizada usando la API de OpenAI (`azureTTS.py` ahora llama al endpoint de OpenAI para generar MP3).
- Archivo `.env` con variables placeholder para `OPENAI_API_KEY`, `OPENAI_TTS_URL`, `TTS_MODEL`, `TRANSCRIBE_MODEL`, `TTS_VOICE`.
- `SECURITY.md` con hallazgos de seguridad y pasos de mitigación.
- `CHANGELOG.md` (este archivo).

### Modificado
- `app.py`: reemplazo de la librería local `whisper` por la API de OpenAI para transcripciones (se usa `OpenAI().audio.transcriptions.create(...)`).
- `processing.py`: ahora importa `text_to_speech` desde `azureTTS.py` (migración a OpenAI TTS).
- `azureTTS.py`: migrado de Azure SDK a llamadas HTTP a OpenAI para generar MP3 y funciones para reproducir el audio.
- `requirements.txt`: simplificado para listar solo dependencias relevantes para el proyecto (OpenAI, Flask, requests, pygame, pandas, openpyxl, numpy, python-dotenv).

### Eliminado
- `elevenlabs.py` y `talk.py`: removidos porque el proyecto centraliza TTS con OpenAI.

### Seguridad
- `pip-audit` reveló una vulnerabilidad en `pip` (GHSA-4xh5-x5gv-qwph). Se sugiere actualizar pip a `>=25.2` dentro del entorno virtual y regenerar `requirements.txt` sin entradas `file://` u `@ file` antes de auditar.

### Cómo verificar
1. Rellenar `.env` con `OPENAI_API_KEY`.
2. Activar tu entorno virtual y actualizar pip:
   python -m pip install --upgrade "pip>=25.2"
3. Instalar dependencias:
   pip install -r requirements.txt
4. Ejecutar pruebas manuales:
   - Arrancar la app: `python app.py` y probar la carga de audio en la ruta `/audio`.
   - Probar `analyze_requisito` vía POST con un JSON `{ "requirement": "Tu requisito" }`.

---
