let clickeado = false;
let mediaRecorder;
let audioChunks = [];
const data = '';
let requirements = []; // Arreglo global para almacenar los requisitos mejorados
let classifications = []; // Arreglo global para almacenar las clasificaciones

const boton = document.getElementById('hola');

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
                            mostrarPopup(data.improved_requirements, data.classifications);
                        } else {
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

    const closeButton = document.createElement('button');
    closeButton.innerText = 'Cerrar';
    closeButton.addEventListener('click', () => {
        document.body.removeChild(popup);
    });
    popup.appendChild(closeButton);

    const list = document.createElement('ul');
    for (let i = 0; i < requirements.length; i++) {
        const listItem = document.createElement('li');
        listItem.dataset.index = i; // Agregamos un atributo de datos para almacenar el índice

        const requirementText = document.createTextNode(`${requirements[i]}`);
        listItem.appendChild(requirementText);

        // Selector para el tipo de requisito
        const typeSelect = document.createElement('select');
        const optionRF = document.createElement('option');
        optionRF.value = 'RF';
        optionRF.text = 'RF';
        if (classifications[i] === 'RF') optionRF.selected = true;

        const optionRNF = document.createElement('option');
        optionRNF.value = 'RNF';
        optionRNF.text = 'RNF';
        if (classifications[i] === 'RNF') optionRNF.selected = true;

        typeSelect.appendChild(optionRF);
        typeSelect.appendChild(optionRNF);
        typeSelect.addEventListener('change', (event) => {
            classifications[i] = event.target.value; // Actualizar la clasificación
        });

        listItem.appendChild(typeSelect);

        const addButton = document.createElement('button');
        addButton.innerText = 'Añadir';
        addButton.addEventListener('click', () => {
            agregarRequisito(classifications[i], requirements[i], i);
        });

        const improveButton = document.createElement('button');
        improveButton.innerText = 'Mejorar';
        improveButton.addEventListener('click', () => {
            mejorarRequisito(i, requirements[i], classifications[i]);
        });

        const sintetizarButton = document.createElement('button');
        sintetizarButton.innerText = 'Sintetizar';
        sintetizarButton.addEventListener('click', () => {
            sintetizarRequisito(requirements[i], i);
        });

        const editButton = document.createElement('button');
        editButton.innerText = 'Editar';
        editButton.addEventListener('click', () => {
            editarRequisito(i, requirements[i]);
        });

        const deleteButton = document.createElement('button');
        deleteButton.innerText = 'Eliminar';
        deleteButton.addEventListener('click', () => {
            eliminarRequisito(i);
        });

        listItem.appendChild(addButton);
        listItem.appendChild(improveButton);
        listItem.appendChild(sintetizarButton);
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

function mejorarRequisito(index, requirement, classification) {
    fetch('/mejorar_requisito', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ requirement: requirement, classification: classification })
    })
        .then(response => response.json())
        .then(data => {
            if (data.result === "ok") {
                alert("Requisito mejorado: " + data.improved_requirement);
                // Actualizar la interfaz con el requisito mejorado
                const listItem = document.querySelector(`.popup ul li[data-index='${index}']`);
                listItem.childNodes[0].nodeValue = `${data.improved_requirement}`;
                requirements[index] = data.improved_requirement; // Actualizar el requisito en el arreglo
            } else {
                alert("Error al mejorar el requisito");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Error al mejorar el requisito");
        });
}

function sintetizarRequisito(requirement, index) {
    fetch('/sintetizar_requisito', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ requirement: requirement })
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === "ok") {
            alert("Requisito sintetizado: " + data.sintetizado);
            // Actualizar la interfaz con el requisito sintetizado
            const listItem = document.querySelector(`.popup ul li[data-index='${index}']`);
            listItem.childNodes[0].nodeValue = `${data.sintetizado}`;
            requirements[index] = data.sintetizado; // Actualizar el requisito en el arreglo
        } else {
            alert("Error al sintetizar el requisito: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error al sintetizar el requisito");
    });
}

function editarRequisito(index, requirement) {
    const listItem = document.querySelector(`.popup ul li[data-index='${index}']`);
    const currentText = requirement;

    // Crear un campo de texto para editar el requisito
    const inputField = document.createElement('input');
    inputField.type = 'text';
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

function eliminarRequisito(index) {
    const listItem = document.querySelector(`.popup ul li[data-index='${index}']`);
    listItem.parentNode.removeChild(listItem);
}
