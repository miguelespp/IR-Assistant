let clickeado = false;
let mediaRecorder;
let audioChunks = [];
const data = '';
let requirements = []; // Arreglo global para almacenar los requisitos mejorados
let classifications = []; // Arreglo global para almacenar las clasificaciones

const boton = document.getElementById('hola');

const micIcon = document.getElementById('micIcon');

// Verifica si el navegador soporta la grabación de audio
if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    console.log("Tu navegador no soporta la grabación de audio");
} else {
    // Solicita acceso al micrófono
    navigator.mediaDevices.getUserMedia({ audio: true, video: false })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);

            // Cuando se recibe datos de audio, los añade a audioChunks
            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            // Cuando se detiene la grabación, envía los datos de audio al servidor
            mediaRecorder.addEventListener("stop", () => {
                const audioData = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append("audio", audioData, 'audio.wav');

                enviarAudio(formData)
                    .then(data => {
                        console.log(data); // Imprimir los datos recibidos desde el servidor

                        if (data && data.classifications && data.classifications.length > 0 && data.classifications[0] !== 'No Clasificado') {
                            requirements = data.improved_requirements; // Almacenar los requisitos mejorados
                            classifications = data.classifications; // Almacenar las clasificaciones
                            boton.style.backgroundColor = 'white';
                            micIcon.innerHTML = '<img class="micro" src="static/microphone.png" alt="wasa">';
                            mostrarPopup(data.improved_requirements, data.classifications);
                        } else {
                            micIcon.innerHTML = '<img class="micro" src="static/microphone.png" alt="wasa">';
                            alert("No se ha podido clasificar el audio");
                        }
                    })
                    .catch(error => {
                        console.error(error);
                        alert("Error al procesar el audio");
                    });

                // Limpia audioChunks para la próxima grabación
                audioChunks = [];
            });
        })
        .catch(error => {
            console.error(error);
            alert("Error al acceder al micrófono");
        });
}

async function enviarAudio(formData) {
    const response = await fetch('/audio', { method: 'POST', body: formData });
    if (!response.ok) {
        throw new Error('Error en la solicitud');
    }
    return response.json();
}

boton.addEventListener("click", function () {
    if (clickeado) {
        boton.style.backgroundColor = 'white';
        console.log("apagado")
        clickeado = false;
        micIcon.innerHTML = '<img src="static/raccoon-dance.gif" alt="Cargando...">'; // Reemplaza 'raccoon-dance.gif' con el nombre de tu archivo GIF
        boton.style.backgroundColor = 'black';
        mediaRecorder.stop();
    } else {
        boton.style.backgroundColor = 'red';
        console.log("encendido")
        clickeado = true;
        mediaRecorder.start();
    }
});

function mostrarPopup(requirements, classifications) {
    const popup = document.createElement('div');
    popup.className = 'popup';

    const list = document.createElement('ul');
    list.className = 'requirements-list';
    for (let i = 0; i < requirements.length; i++) {
        const listItem = document.createElement('li');
        listItem.dataset.index = i; // Agregamos un atributo de datos para almacenar el índice

        const mainContent = document.createElement('p');

        mainContent.innerText = `${requirements[i]}`
        listItem.appendChild(mainContent);


        const addButton = document.createElement('button');
        addButton.innerText = 'Añadir';
        addButton.addEventListener('click', () => {
            agregarRequisito(classifications[i], requirements[i], i);
            document.body.removeChild(popup);
        });



        const analyzeButton = document.createElement('button');
        analyzeButton.innerText = 'Analizar';
        analyzeButton.addEventListener('click', () => {
            analyzeRequisito(requirements[i], i);
        });

        const editButton = document.createElement('button');
        editButton.innerText = 'Editar';
        editButton.addEventListener('click', () => {
            editarRequisito(i, requirements[i]);
        });

        const deleteButton = document.createElement('button');
        deleteButton.innerText = 'Descartar';
        deleteButton.addEventListener('click', () => {
            document.body.removeChild(popup);
        });

        listItem.appendChild(addButton);

        listItem.appendChild(analyzeButton);
        listItem.appendChild(editButton);
        listItem.appendChild(deleteButton);

        list.appendChild(listItem);
    }

    popup.appendChild(list);
    document.body.appendChild(popup);
}

function agregarRequisito(classification, requirement, index) {
    const prefix = classification === 'RF' ? 'RF' : 'RNF';
    const list = document.getElementById(classification + '-list');
    const element = document.createElement('li');
    element.innerText = `${prefix}: ${requirement}`;
    element.className = classification;
    list.append(element);

    // Eliminar el requisito de la lista del pop-up
    const listItem = document.querySelector(`.popup ul li[data-index='${index}']`);
    listItem.parentNode.removeChild(listItem);
}

function analyzeRequisito(requirement, index) {
    fetch('/analyze_requisito', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ requirement: requirement })
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === "ok") {
            const listItem = document.querySelector(`.popup ul`);
            const container = document.createElement('ul');
            const recomendations = data.sintetizado.split("\n");
            recomendations.forEach(element => {
                const createItem = document.createElement('li');
                createItem.appendChild(document.createTextNode(`${element}`));
                container.appendChild(createItem);
            });
            container.style.backgroundColor = 'lightblue';
            listItem.appendChild(container);
        } else {
            alert("Error al sintetizar el requisito: " + data.message);
        }
        console.log(data)
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error al sintetizar el requisito");
    });
}

function editarRequisito(index, requirement) {
    const listItem = document.querySelector(`.popup ul li[data-index='${index}']`);
    const currentText = requirement;

    // Crear un campo de texto más grande para editar el requisito
    const inputField = document.createElement('textarea');
    inputField.className = 'edit-field';  // Añadir una clase para aplicar estilos
    inputField.value = currentText;
    listItem.replaceChild(inputField, listItem.childNodes[0]);

    // Cambiar los botones de acción
    const saveButton = document.createElement('button');
    saveButton.innerText = 'Guardar';
    saveButton.addEventListener('click', () => {
        const newText = inputField.value;
        listItem.replaceChild(document.createTextNode(`${newText}`), inputField);
        listItem.replaceChild(editButton, saveButton);
        requirements[index] = newText; // Actualizar el requisito en el arreglo
    });

    const editButton = listItem.childNodes[1];
    listItem.replaceChild(saveButton, editButton);
}

function exportToExcel() {
    // Preparar los datos a exportar
    const dataToExport = {
        improved_requirements: requirements,
        classifications: classifications
    };

    fetch('/export_to_excel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToExport)
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(new Blob([blob]));
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'requisitos.xlsx'; // Nombre del archivo Excel
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Error al exportar a Excel:', error);
        alert('Error al exportar a Excel');
    });
}
