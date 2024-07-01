# processing.py
from classification import classify_requirement
from openai import OpenAI
import re
from talk import Talk

# Configuración de FakeYou
FAKEYOU_USERNAME = ""
FAKEYOU_PASSWORD = ""
MODEL_NAME = 'auronplay' #no hace nd xd

# Inicializar la clase Talk
talker = Talk(FAKEYOU_USERNAME, FAKEYOU_PASSWORD, MODEL_NAME)

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
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return requirement #response.choices[0].message.content.strip()


def analyze_requirement(requirement):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en análisis de requisitos."},
                {"role": "user", "content": f"¿El siguiente requisito es ambiguo? (sin exagerar): {requirement}.Si es ambiguo (exagerado), Formula preguntas en una lista de maximo 2 puntos para aclarar el requisito (no digas si es ambiguo solo manda las preguntas si lo es); si no es muy ambiguo di 'Ta bien'."}
            ],
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
        )
        owa = response.choices[0].message.content.strip()
        # Hablar el texto transcrito usando FakeYou
        talker.talk(owa)
        return response.choices[0].message.content.strip()
    

