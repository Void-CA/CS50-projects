function validarFormulario() {
    // Obtener los valores de los campos de entrada
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmation').value;

    // Comparar los valores
    if (password !== confirmPassword) {
        // Utilizar SweetAlert2 para mostrar el mensaje de error
        mensajeError("Las contraseñas no coinciden");

        return false; // Evitar que el formulario se envíe
    }

    // Si las contraseñas coinciden, el formulario se enviará
    return true;
}

function facturaAñadida() {
    mensajeExito("Factura añadida correctamente");
}

function mensajeError(mensaje) {
    Swal.fire({
        icon: 'error',
        title: 'Error',
        text: mensaje,
    });
}

function mensajeExito(mensaje) {
    Swal.fire({
        icon: 'success',
        title: 'Operación Exitosa',
        text: mensaje,
    });

    return true; // Para permitir que el formulario se envíe después del mensaje exitoso
}

document.getElementById('formulario-busqueda').addEventListener('input', function() {
    realizarBusqueda();
});

function realizarBusqueda() {
    var id = document.getElementById('campo_id').value;
    var categoria = document.getElementById('campo_categoria').value;
    var monto_min = document.getElementById('campo_monto_min').value;
    var monto_max = document.getElementById('campo_monto_max').value;

    // Realiza una solicitud AJAX al servidor
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'campo_id=' + encodeURIComponent(id) +
              '&campo_categoria=' + encodeURIComponent(categoria) +
              '&campo_monto_min=' + encodeURIComponent(monto_min) +
              '&campo_monto_max=' + encodeURIComponent(monto_max),
    })
    .then(response => response.json())
    .then(data => mostrarResultados(data))
    .catch(error => console.error('Error:', error));
}

function mostrarResultados(resultados) {
    var resultadosContainer = document.getElementById('resultados-busqueda');
    
    // Limpiar resultados anteriores
    resultadosContainer.innerHTML = '';

    resultados.forEach(function(resultado) {
        resultadosContainer.innerHTML += '<div class="resultado">' +
                                        '<p class = "text-justified"> <span>ID</span>: ' + resultado.id + '</p>' +
                                        '<p class = "text-justified"> <span>Estado</span>: ' + resultado.status + '</p>' +
                                        '<p class = "text-justified"> <span>Categoría</span>: ' + resultado.category + '</p>' +
                                        '<p class = "text-justified"> <span>Monto</span>: $' + resultado.amount + '</p>' +
                                        '<p class = "text-justified"> <span>Descripción</span>: ' + resultado.description + '</p>' +
                                        '</div>';
    });

}