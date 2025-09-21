// app/piedrapapeltijera/static/piedrapapeltijera/js/play_game.js

window.onload = function() {
    restartGame();
};

const choiceBtns = document.querySelectorAll('.choice-btn');
const resetBtn = document.querySelector('.reset');
const giveupBtn = document.querySelector('.giveup');

const playerScoreSpan = document.getElementById('current-score');
const playerWinsSpan = document.getElementById('player-wins');
const machineWinsSpan = document.getElementById('machine-wins');
const drawsSpan = document.getElementById('draws');
const playerChoiceP = document.getElementById('player-choice');
const machineChoiceP = document.getElementById('machine-choice');
const resultMessageH3 = document.getElementById('result-message');


function restartGame() {
    fetch('/piedrapapeltijera/action/restart/')
        .then(response => response.json())
        .then(data => {
            console.log('Juego Reiniciado:', data.message);
            updateUI({
                score: 0,
                player_wins: 0,
                machine_wins: 0,
                draws: 0,
                player_choice: '?',
                machine_choice: '?',
                result: 'start'
            });
        })
        .catch(error => console.error('Error al reiniciar el juego:', error));
}


function clientPlay(event) {
    const playerChoice = event.currentTarget.dataset.choice;
    fetch(`/piedrapapeltijera/play/${playerChoice}/`)
        .then(response => response.json())
        .then(data => {
            console.log('Datos recibidos:', data);
            if (data.status === 'error') {
                resultMessageH3.textContent = data.message;
                return;
            }
            updateUI(data);
        })
        .catch(error => console.error('Error al realizar la jugada:', error));
}


function updateUI(data) {
    playerScoreSpan.textContent = data.score;
    playerWinsSpan.textContent = data.player_wins;
    machineWinsSpan.textContent = data.machine_wins;
    drawsSpan.textContent = data.draws;
    playerChoiceP.textContent = `Tu elección: ${data.player_choice}`;
    machineChoiceP.textContent = `Máquina: ${data.machine_choice}`;
    
    switch (data.result) {
        case 'win':
            resultMessageH3.textContent = '¡Ganaste esta ronda!';
            break;
        case 'defeat':
            resultMessageH3.textContent = '¡Perdiste! Intenta de nuevo.';
            break;
        case 'draw':
            resultMessageH3.textContent = '¡Empate!';
            break;
        case 'start':
            resultMessageH3.textContent = '¡Elige tu movimiento!';
            break;
    }
}


function giveUp() {
    fetch('/piedrapapeltijera/action/giveup/')
        .then(response => response.json())
        .then(data => {
            alert(`Tu puntaje final es: ${data.score}`);
            restartGame();
        })
        .catch(error => console.error('Error al rendirse:', error));
}


// Asignar eventos a los botones
choiceBtns.forEach(btn => {
    btn.addEventListener('click', clientPlay);
});

resetBtn.addEventListener('click', restartGame);

giveupBtn.addEventListener('click', giveUp);