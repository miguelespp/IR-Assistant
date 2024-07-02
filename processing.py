# processing.py
from classification import classify_requirement
from openai import OpenAI
import re


#from elevenlabs import text_to_speech, play_and_delete_audio

from azureTTS import text_to_speech, play_and_delete_audio

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
                {"role": "system", "content": "Eres un analista de requisitos flexible y comprensivo."},
                {"role": "user", "content": f"Soy un cliente no muy experto en el desarrollo de software. Ten en cuenta eso y sé flexible: ¿El siguiente requisito es ambiguo? (sin ser estricto): {requirement}. SI NO ES AMBIGUO DI 'Ta bien'; Si es muy ambiguo, formula una pregunta que no sea de sí o no para aclarar el requisito, sin hacer preguntas implícitamente respondidas en el requisito y manteniéndolo simple."}
            ],
            max_tokens=40,
            n=1,
            stop=None,
            temperature=0.7,
        )
        owa = response.choices[0].message.content.strip()
        # Hablar el texto transcrito usando azure
        text_to_speech(owa)
        # Play the audio and delete it afterwards
        #play_and_delete_audio("output.mp3")

        return response.choices[0].message.content.strip()
    

