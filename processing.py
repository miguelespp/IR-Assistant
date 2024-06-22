# processing.py
from classification import classify_requirement
from openai import OpenAI
import re

client = OpenAI()


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
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Eres un experto en análisis de requisitos {classification}."},
            {"role": "user",
             "content": f"Reformula el siguiente requisito sin añadir opiniones ni explicaciones, solo el requisito mejorado: {requirement}"}
        ],
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def analyze_requirement(requirement):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Eres un experto en la especificacion de requisitos."},
            {"role": "user",
             "content": f"Dame las posibles ambigüedades o problemas del requisito {requirement} , en una lista de maximo 3 puntos"}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
    # return [choice.message.content.strip() for choice in response.choices]
