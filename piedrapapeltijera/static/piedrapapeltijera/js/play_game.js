// Piedra, Papel o Tijera 

loadingBtn.addEventListener('click', ()=>{
    restartGame();
    show_dialogue('inicio', 'piedrapapeltijera');
})

const choiceBtns = document.querySelectorAll('.choice-btn');
const resetButton = document.querySelector('.resetbtn');
const giveupBtn = document.querySelector('.giveup');

const playerScoreSpan = document.getElementById('current-score');
const playerWinsSpan = document.getElementById('player-wins');
const machineWinsSpan = document.getElementById('machine-wins');
const drawsSpan = document.getElementById('draws');
const playerChoiceP = document.getElementById('player-choice');
const machineChoiceP = document.getElementById('machine-choice');
const resultMessageH3 = document.getElementById('result-message');

let gameFinished = false;

const choiceEmojis = {
    piedra: "✊",
    papel: "✋",
    tijera: "✌️"
};

function capitalize(word) {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

function restartGame() {
    fetch('/piedrapapeltijera/action/restart/')
        .then(response => response.json())
        .then(data => {
            console.log('Juego Reiniciado:', data.message);
            gameFinished = false;
            enableChoiceButtons(true);
            updateUI({
                player_score: 0,
                player_wins: 0,
                machine_wins: 0,
                draws: 0,
                player_choice: '❓',
                machine_choice: '❓',
                result: 'start'
            });
        })
        .catch(error => console.error('Error al reiniciar el juego:', error));
}

function clientPlay(event) {
    if (gameFinished) {
        resultMessageH3.textContent = "El juego ha terminado. Reinicia para jugar de nuevo.";
        return;
    }

    const playerChoice = event.currentTarget.dataset.choice;
    fetch(`/piedrapapeltijera/play/${playerChoice}/`)
        .then(response => response.json())
        .then(data => {
            console.log('Datos recibidos:', data);

            if (data.status === 'error') {
                resultMessageH3.textContent = data.message;
                return;
            }

            // Mostrar el modal solo si terminó la partida
            if (data.status === 'finished' || data.rounds_played >= data.rounds_limit) {
                gameFinished = true;
                enableChoiceButtons(false);
                resultMessageH3.textContent = data.message || "¡Juego terminado! Reinicia o ríndete.";
                console.log(data);
                showModalScreen('piedrapapeltijera', data); // <-- ESTA LÍNEA ES CLAVE
                return;
            }

            updateUI(data);
        })
        .catch(error => console.error('Error al realizar la jugada:', error));
}

function updateUI(data) {
    playerScoreSpan.textContent = data.player_score;
    playerWinsSpan.textContent = data.player_wins;
    machineWinsSpan.textContent = data.machine_wins;
    drawsSpan.textContent = data.draws;

    // Mostrar elección del usuario con emoji y mayúscula
    if (data.player_choice) {
        playerChoiceP.textContent = `Tu elección: ${choiceEmojis[data.player_choice] || ""} ${capitalize(data.player_choice)}`;
    } else {
        playerChoiceP.textContent = "Tu elección: ❓";
    }

    // Mostrar elección de la máquina con emoji y mayúscula
    if (data.machine_choice) {
        machineChoiceP.textContent = `Máquina: ${choiceEmojis[data.machine_choice] || ""} ${capitalize(data.machine_choice)}`;
    } else {
        machineChoiceP.textContent = "Máquina: ❓";
    }
    
    // Animaciones de resultado
    resultMessageH3.classList.remove('result-animate', 'shake');
    void resultMessageH3.offsetWidth; // fuerza reflow

    switch (data.result) {
        case 'win':
            resultMessageH3.textContent = 'Ganaste esta ronda! 🎉';
            resultMessageH3.classList.add('shake');
            break;
        case 'defeat':
            resultMessageH3.textContent = 'Perdiste esta ronda 💔';
            break;
        case 'draw':
            resultMessageH3.textContent = 'Empate 🤝';
            break;
        case 'start':
            resultMessageH3.textContent = 'Elige tu movimiento!';
            break;
    }
    resultMessageH3.classList.add('result-animate');

    if (data.result === 'win') {
        show_dialogue('victoria', 'piedrapapeltijera');
    }
    if (data.result === 'defeat') {
        show_dialogue('derrota', 'piedrapapeltijera');
    }
    if (data.result === 'draw') {
        show_dialogue('empate', 'piedrapapeltijera');
    }
}

function giveUp() {
    fetch('/piedrapapeltijera/action/giveup/')
        .then(response => response.json())
        .then((data) => {
            showModalScreen('piedrapapeltijera', data); // <-- AQUÍ
            alert(`Tu puntaje final es: ${data.player_score}`);
            restartGame();
        })
        .catch(error => console.error('Error al rendirse:', error));
}

function enableChoiceButtons(enable) {
    choiceBtns.forEach(btn => {
        btn.disabled = !enable;
    });
}

// async function show_dialogue(category, game) {
//     try {
//         const response = await fetch(`/globals/get_dialogue/${category}/${game}/`);
//         const result = await response.json();
//         if (result.status === 'ok' && result.dialogue && result.dialogue.text) {
//             document.getElementById('dialogue-text').textContent = result.dialogue.text;
//         } else {
//             document.getElementById('dialogue-text').textContent = "¡Suerte!";
//         }
//     } catch (err) {
//         document.getElementById('dialogue-text').textContent = "¡Suerte!";
//     }
// }

// Asignar eventos a los botones
choiceBtns.forEach(btn => {
    btn.addEventListener('click', clientPlay);
});
resetButton.addEventListener('click', restartGame);
giveupBtn.addEventListener('click', function() {
    giveUp();
    show_dialogue('rendicion', 'piedrapapeltijera');
});
