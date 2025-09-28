// adivinarnumero/static/adivinarnumero/js/play_game.js

const MAX_ATTEMPTS_CLIENT = 7; // Basado en NUM_ATTEMPTS de constants.py
let timer = 0;
let interval;
let targetNumber = null; // Para almacenar el número secreto si se recibe tras perder
let gameFinished = false;

window.onload = () => {
    // Inicialización al cargar la página
    document.getElementById("max-attempts").textContent = MAX_ATTEMPTS_CLIENT;
    
    // Inicia el juego y el temporizador
    restartGame(); 
};

/**
 * Inicia o reinicia el temporizador.
 */
function startTimer() {
    clearInterval(interval);
    timer = 0;
    gameFinished = false;
    document.getElementById("timer").textContent = timer;
    
    // El temporizador se ejecuta cada segundo
    interval = setInterval(() => {
        if (!gameFinished) {
            timer++;
            document.getElementById("timer").textContent = timer;
        }
    }, 1000);
}

/**
 * Reinicia la partida en el backend y actualiza el frontend.
 */
function restartGame() {
    fetch("/adivinarnumero/action/restart/")
        .then(res => {
            // Verifica si la respuesta HTTP fue exitosa (código 200-299)
            if (!res.ok) {
                // Si hay un error 4xx o 5xx, arrojar un error para el catch
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(() => {
            // Reiniciar estados del juego
            targetNumber = null;
            gameFinished = false;

            // Limpiar la interfaz
            document.getElementById("current-score").textContent = "0";
            document.getElementById("attempts").textContent = "0";
            document.getElementById("max-attempts").textContent = MAX_ATTEMPTS_CLIENT;
            document.getElementById("status-message").textContent = "Ingresa un número del 1 al 100";
            document.getElementById("guess-input").value = "";
            document.getElementById("guess-input").disabled = false;
            document.getElementById("guess-btn").disabled = false;
            
            // Limpiar y resetear historial, COMPROBANDO SI EL ELEMENTO EXISTE
            const historyList = document.getElementById("guess-history");
            if (historyList) {
                historyList.innerHTML = '';
            }
            
            // Eliminar la clase clickeable
            document.getElementById("status-message").classList.remove('revealable');

            startTimer();
        })
        .catch(error => {
            console.error("Error al reiniciar el juego:", error);
            // Mensaje más específico 
            document.getElementById("status-message").textContent = "Error de comunicación con el servidor al reiniciar. Revisa la consola para el error específico (404/500/JSON).";
        });
}

/**
 * Maneja el intento de adivinar el número.
 */
function guessNumber() {
    const number = parseInt(document.getElementById("guess-input").value);
    
    // Validaciones básicas
    if (isNaN(number) || number < 1 || number > 100) {
        document.getElementById("status-message").textContent = "Ingresa un número válido (1-100).";
        return;
    }
    
    if (gameFinished) {
        document.getElementById("status-message").textContent = "¡Juego terminado! Presiona 'Reiniciar'.";
        return;
    }

    // Llama a la vista de Django con el número
    fetch(`/adivinarnumero/play/${number}/`)
        .then(res => {
            if (!res.ok) {
                // Si hay un error 4xx o 5xx, arrojar un error para el catch
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            // 1. Actualizar historial con el nuevo intento
            updateGuessHistory(number, data.result);

            // 2. Actualizar estados del juego
            document.getElementById("current-score").textContent = data.score;
            document.getElementById("attempts").textContent = data.attempts;
            document.getElementById("max-attempts").textContent = data.max_attempts;
            document.getElementById("timer").textContent = data.elapsed;
            
            // Limpiar el input para el siguiente intento
            document.getElementById("guess-input").value = "";

            // 3. Manejar el resultado y mensaje
            let message = "";
            let isGameOver = false;

            if (data.result === "low") {
                message = "El número es mayor 🔼";
            } else if (data.result === "high") {
                message = "El número es menor 🔽";
            } else if (data.result === "correct") {
                message = `¡Correcto! 🎉 Puntaje: ${data.score}`;
                isGameOver = true;
            } else if (data.result === "fail") {
                // Guarda el número secreto para revelarlo después
                targetNumber = data.target; 
                message = "¡Se acabaron los intentos! 😢 Haz clic para ver el número.";
                isGameOver = true;
                
                // Hace el mensaje clickeable
                document.getElementById("status-message").classList.add('revealable');
            }

            document.getElementById("status-message").textContent = message;

            if (isGameOver) {
                gameFinished = true;
                clearInterval(interval);
                document.getElementById("guess-input").disabled = true;
                document.getElementById("guess-btn").disabled = true;
            }
        })
        .catch(error => {
            console.error("Error al verificar el intento:", error);
            document.getElementById("status-message").textContent = "Error de comunicación con el servidor. Intenta reiniciar.";
        });
}

/**
 * Añade el número intentado al historial.
 * @param {number} number - El número que el usuario intentó.
 * @param {string} result - El resultado del intento ('low', 'high', 'correct', 'fail').
 */
function updateGuessHistory(number, result) {
    const historyList = document.getElementById("guess-history");
    
    // Si el elemento no existe, sal de la función. Esto es una capa de seguridad.
    if (!historyList) return; 

    const listItem = document.createElement('li');
    
    // Añade el número
    listItem.textContent = number;
    
    // Opcionalmente, puedes darle un estilo basado en si fue alto o bajo
    if (result === 'low') {
        listItem.style.backgroundColor = '#1f78b4'; // Azul
    } else if (result === 'high') {
        listItem.style.backgroundColor = '#e31a1c'; // Rojo
    } else if (result === 'correct') {
        listItem.style.backgroundColor = '#33a02c'; // Verde
    }

    // Insertar el nuevo elemento al principio (para que el último intento esté arriba)
    historyList.prepend(listItem);
}


/**
 * Maneja la rendición del jugador.
 */
function giveUp() {
    if (gameFinished) {
        restartGame();
        return;
    }
    
    fetch("/adivinarnumero/action/giveup/")
        .then(res => res.json())
        .then(data => {
            document.getElementById("current-score").textContent = data.score;
            document.getElementById("status-message").textContent = `¡Te has rendido! Puntaje guardado: ${data.score}`;
            gameFinished = true;
            clearInterval(interval);
            document.getElementById("guess-input").disabled = true;
            document.getElementById("guess-btn").disabled = true;
        })
        .catch(error => {
            console.error("Error al rendirse:", error);
            document.getElementById("status-message").textContent = "Error al guardar el puntaje.";
        });
}

/**
 * Función para revelar el número secreto si el juego terminó en derrota.
 */
function revealSecretNumber() {
    const messageElement = document.getElementById("status-message");
    
    // Solo revela si el juego terminó por derrota y el número está disponible
    if (gameFinished && targetNumber !== null && messageElement.classList.contains('revealable')) {
        messageElement.textContent = `¡El número era ${targetNumber}!`;
        messageElement.classList.remove('revealable'); // Evita más clics
    }
}


// Asignación de Event Listeners
document.getElementById("guess-btn").addEventListener("click", guessNumber);
document.querySelector(".reset").addEventListener("click", restartGame);
document.querySelector(".giveup").addEventListener("click", giveUp);

// Evento para revelar el número secreto (nuevo)
document.getElementById("status-message").addEventListener("click", revealSecretNumber);
