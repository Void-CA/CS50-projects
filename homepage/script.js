var data = [
    "I have broken broken my leg once",
    "I want to study the Data Science program of Harvard",
    "My favorite movie is Coraline",
    "I love Jujutsu Kaisen",
    "I want to travel to Amsterdam",
    "My favorite dish is Spaghetti",
    "I want to have a daughter called Amaris",
    "My group of friends is called Chancho con Yuca"
];

// Función para mostrar un dato al azar en el modal
function mostrarDatoEnModal() {
    // Obtén un índice aleatorio para seleccionar un dato al azar
    var indiceAleatorio = Math.floor(Math.random() * data.length);

    // Obtén el elemento donde mostrar el dato en el modal
    var elementoMostrado = document.getElementById("datoMostrado");

    // Muestra el dato en el elemento del modal
    elementoMostrado.textContent = data[indiceAleatorio];
}

// Agrega un evento de clic al botón para mostrar el modal
document.querySelector('.btn-primary').addEventListener('click', mostrarDatoEnModal);
