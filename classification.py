from openai import OpenAI

client = OpenAI()


def classify_requirement(requirement):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un experto en clasificación de requisitos."},
            {"role": "user", "content": f"Clasifica el siguiente requisito únicamente como 'RF' (Requisito Funcional), 'RNF' (Requisito No Funcional) o 'No Clasificado': {requirement}. Responde solo con una de esas opciones y nada más."}
        ],
        max_tokens=50,  # Aumentamos el número máximo de tokens para obtener una respuesta más detallada
        n=1,
        stop=None,
        temperature=0.3,  # Reducimos la temperatura para obtener respuestas más precisas
    )
    classification = response.choices[0].message.content.strip()
    
    if classification in ["RF", "RNF", "NO CLASIFICADO"]:
        return classification
    else:
        return "No Clasificado"
