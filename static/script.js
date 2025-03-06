async function uploadPDF() {
    let fileInput = document.getElementById('pdfInput');
    if (fileInput.files.length === 0) {
        alert('Selecciona un archivo PDF.');
        return;
    }

    let formData = new FormData();
    formData.append('file', fileInput.files[0]);

    let response = await fetch('/upload/', {
        method: 'POST',
        body: formData,
    });

    let resultDiv = document.getElementById('result');
    resultDiv.innerHTML = 'Procesando...';

    if (response.ok) {
        let data = await response.json();
        resultDiv.innerHTML = `<h2>Firmas Encontradas</h2>`;

        data.firmas.forEach((firma) => {
            resultDiv.innerHTML += `<p><strong>Firmante:</strong> ${firma.firmante}</p>`;
            resultDiv.innerHTML += `<p><strong>Fecha:</strong> ${firma.fecha}</p>`;
            resultDiv.innerHTML += `<p><strong>Razón:</strong> ${firma.razon}</p>`;
            resultDiv.innerHTML += `<hr>`;
        });

        resultDiv.innerHTML += `<h2>Imágenes Extraídas</h2>`;
        data.imagenes.forEach((img) => {
            resultDiv.innerHTML += `<img src="${img}" width="200"><br>`;
        });
    } else {
        resultDiv.innerHTML = 'Error al procesar el archivo.';
    }
}
