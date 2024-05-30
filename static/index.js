let clickeado = false;
let mediaRecorder;
let audioChunks = [];
const data = '';

const boton = document.getElementById('hola');

// Verifica si el navegador soporta la grabación de audio
if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    console.log("Tu navegador no soporta la grabación de audio");
} else {
    // Solicita acceso al micrófono
    navigator.mediaDevices.getUserMedia({ audio: true, video: false})
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
                    .then(r => console.log(r))
                    .catch(error => console.error(error));


                // Limpia audioChunks para la próxima grabación
                audioChunks = [];
            });
        })
        .catch(error => console.error(error));
}

async function enviarAudio(formData)
{
    await fetch('/audio', { method: 'POST', body: formData })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data)
                        if (data.type !== 'No Clasificado'){
                            let type = 'RNF-list'
                            const list = document.getElementById(data.type + '-list');
                            const element = document.createElement('li');
                            // Mostrar los datos en el elemento div
                            element.innerText = data.text;
                            element.className = data.type;
                            list.append(element);

                            return data.text;
                        }else{
                            alert("No se ha podido clasificar el audio")
                        }

                    })
                    .catch(error => console.error(error));
}
boton.addEventListener("click", function() {
    if (clickeado) {
        boton.style.backgroundColor = 'white';
        console.log("apagado")
        clickeado = false;
        mediaRecorder.stop();
    } else {
        boton.style.backgroundColor= 'red';
        console.log("encendido")
        clickeado = true;
        mediaRecorder.start();
    }
});