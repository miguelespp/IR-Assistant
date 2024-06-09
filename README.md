# Asistente Virtual para Estructuración y Clasificación de Requisitos

## Descripción

Esta aplicación consiste en un asistente virtual que escucha conversaciones y estructura y clasifica los requisitos. Está desarrollada en Python utilizando Flask para la interfaz web y modelos de inteligencia artificial para el procesamiento de lenguaje natural.

## Características

- **Escucha de Conversaciones**: El asistente puede escuchar y transcribir conversaciones en tiempo real.
- **Estructuración de Requisitos**: Una vez transcrita la conversación, el asistente identifica y estructura los requisitos mencionados.
- **Clasificación de Requisitos**: Los requisitos se clasifican en diferentes categorías para facilitar su gestión.
- **Interfaz Web**: Una interfaz sencilla y amigable para interactuar con el asistente.

## Tecnologías Utilizadas

- Python
- Flask
- Modelos de IA (NLP, Speech-to-Text)
- HTML/CSS/JavaScript

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/miguelespp/IR-Assistant.git
    cd IR-Assistant
    ```

2. Crea un entorno virtual e instala las dependencias:

    ```bash
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

3. Configura las variables de entorno necesarias (API keys, configuración del modelo, etc.) en un archivo `.env` en la raíz del proyecto.

4. Inicia la aplicación:

    ```bash
    flask run
    ```

## Uso

1. Abre tu navegador web y ve a `http://localhost:5000`.
2. Inicia una nueva sesión de conversación.
3. Permite al asistente escuchar la conversación.
4. Visualiza los requisitos estructurados y clasificados en la interfaz.

## Estructura del Proyecto

- `app.py`: Archivo principal que contiene la configuración de Flask y las rutas de la aplicación.
- `static/`: Archivos estáticos (CSS, JavaScript).
- `templates/`: Plantillas HTML para la interfaz web.
- `requirements.txt`: Lista de dependencias del proyecto.
