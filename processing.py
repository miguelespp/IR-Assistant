# processing.py
from classification import classify_requirement
import openai
import re

openai.api_key = "TU-KEY-API-XD"

def improve_and_classify_requirements(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    improved_requirements = []
    classifications = []

    for sentence in sentences:
        classification = classify_requirement(sentence)
        improved_requirement = improve_requirement(sentence, classification)

        improved_requirements.append(improved_requirement)
        classifications.append(classification)

    return improved_requirements, classifications

def improve_requirement(requirement, classification):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Eres un experto en análisis de requisitos {classification}."},
            {"role": "user", "content": f"Reformula el siguiente requisito sin añadir opiniones ni explicaciones, solo el requisito mejorado: {requirement}"}
        ],
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

def sintetizar_requisito(requirement):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un experto en síntesis de información."},
            {"role": "user", "content": f"Resumir el siguiente requisito para hacerlo más preciso y corto: {requirement}"}
        ],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()
