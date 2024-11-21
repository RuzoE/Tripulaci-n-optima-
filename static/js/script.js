// Función para enviar el formulario
async function enviarFormulario() {
    const formData = {
        vuelos_cortos: document.getElementById("vuelos_cortos").value,
        vuelos_medios: document.getElementById("vuelos_medios").value,
        vuelos_largos: document.getElementById("vuelos_largos").value,
        duracion_corto: document.getElementById("duracion_corto").value,
        duracion_medio: document.getElementById("duracion_medio").value,
        duracion_largo: document.getElementById("duracion_largo").value,
        costo_piloto: document.getElementById("costo_piloto").value,
        costo_cabina: document.getElementById("costo_cabina").value
    };

    // Validar los campos antes de enviar
    if (!validarCampos(formData)) {
        return; // Detener el envío si hay errores
    }

    try {
        const response = await fetch('https://tripulacion-optima.onrender.com/optimizar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            const result = await response.json();
            mostrarResultado(result);
        } else {
            document.getElementById("resultado").innerText = "Error al calcular la asignación.";
            console.error("Error en la respuesta del servidor:", response.statusText);
        }
    } catch (error) {
        console.error("Error en la solicitud:", error);
        document.getElementById("resultado").innerText = "No se pudo conectar con el servidor.";
    }
}

// Función para validar los campos del formulario
function validarCampos(formData) {
    let errores = [];

    // Validar números negativos
    for (const [campo, valor] of Object.entries(formData)) {
        if (isNaN(valor) || valor < 0) {
            errores.push(`El campo ${campo.replace('_', ' ')} no puede ser negativo ni contener caracteres no numéricos.`);
        }
    }

    // Validar rangos lógicos
    if (formData.duracion_corto > 3) {
        errores.push("La duración de vuelos cortos no puede superar las 3 horas.");
    }
    if (formData.duracion_medio < 3 || formData.duracion_medio > 6) {
        errores.push("La duración de vuelos medios debe estar entre 3 y 6 horas.");
    }
    if (formData.duracion_largo < 6) {
        errores.push("La duración de vuelos largos debe ser mayor o igual a 6 horas.");
    }

    if (formData.costo_piloto < 10 || formData.costo_piloto > 500) {
        errores.push("El costo por hora de piloto debe estar entre 10 y 500.");
    }
    if (formData.costo_cabina < 10 || formData.costo_cabina > 500) {
        errores.push("El costo por hora de personal de cabina debe estar entre 10 y 500.");
    }

    // Mostrar errores al usuario
    if (errores.length > 0) {
        alert("Errores detectados:\n" + errores.join("\n"));
        return false;
    }

    return true;
}

// Función para formatear valores en pesos colombianos
function formatToCOP(value) {
    const formatter = new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 2
    });
    return formatter.format(value);
}

// Función para mostrar el resultado en el DOM
function mostrarResultado(result) {
    let resultadoHTML = `<h4>Asignación óptima de tripulación y costo diario:</h4>`;
    resultadoHTML += `<p>Pilotos para vuelos cortos: ${result["Pilotos para vuelos cortos"]}</p>`;
    resultadoHTML += `<p>Personal de cabina para vuelos cortos: ${result["Personal de cabina para vuelos cortos"]}</p>`;
    resultadoHTML += `<p>Pilotos para vuelos medios: ${result["Pilotos para vuelos medios"]}</p>`;
    resultadoHTML += `<p>Personal de cabina para vuelos medios: ${result["Personal de cabina para vuelos medios"]}</p>`;
    resultadoHTML += `<p>Pilotos para vuelos largos: ${result["Pilotos para vuelos largos"]}</p>`;
    resultadoHTML += `<p>Personal de cabina para vuelos largos: ${result["Personal de cabina para vuelos largos"]}</p>`;
    resultadoHTML += `<p><strong>Costo total diario: ${formatToCOP(result["Costo total diario"])}</strong></p>`;

    document.getElementById("resultado").innerHTML = resultadoHTML;
}

// Función para manejar el modal de ayuda
document.addEventListener("DOMContentLoaded", function() {
    const helpModal = new bootstrap.Modal(document.getElementById('helpModal'), {});

    // Botón de ayuda
    const helpButton = document.getElementById('helpButton');
    if (helpButton) {
        helpButton.addEventListener('click', function() {
            helpModal.show();
        });
    }
});
