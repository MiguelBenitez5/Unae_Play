let boardState = [];

// 🔹 Inicializa juego: dibuja tablero y pide datos al servidor
async function startGame(rows = 8, cols = 8) {
    drawBoard(rows, cols); // tablero limpio con '?'
    try {
        const response = await fetch('/buscaminas/start/');
        if (!response.ok) throw new Error('Server returned ' + response.status);
        const data = await response.json();
        console.log('Game started:', data);
        show_dialogue('inicio', 'buscaminas')
        boardState = data.board || boardState;
        updateBoard();
    } catch (err) {
        console.error(err);
    }
}

// 🔹 Revelar celda
async function reveal(r, c) {
    try {
        const response = await fetch(`/buscaminas/reveal/${r}/${c}/`);
        if (!response.ok) throw new Error('Server returned ' + response.status);
        const data = await response.json();
        console.log(data);

        boardState = data.board;
        updateBoard();

        if (data.game_status === "defeat") {
            // setTimeout(() => startGame(boardState.length, boardState[0].length), 2000); //here dialogos y modal
            show_dialogue('derrota', 'buscaminas')
            showModalScreen('buscaminas', data)
        } else if (data.game_status === "win") {
            // setTimeout(() => startGame(boardState.length, boardState[0].length), 1500); //here dialogos y modal
            show_dialogue('victoria', 'buscaminas')
            showModalScreen('buscaminas', data)
        }
    } catch (err) {
        console.error(err);
    }
}

// 🔹 Dibuja tablero inicial con '?'
function drawBoard(rows, cols) {
    const grid = document.getElementById("grid");
    grid.innerHTML = '';
    boardState = Array.from({ length: rows }, () => Array(cols).fill(null));

    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const cell = document.createElement("div");
            cell.className = "cell";
            cell.dataset.row = r;
            cell.dataset.col = c;
            cell.textContent = "?";
            cell.addEventListener('click', () => reveal(r, c));
            grid.appendChild(cell);
        }
    }
}

// 🔹 Actualiza el tablero según boardState
function updateBoard() {
    const grid = document.getElementById("grid");
    const rows = boardState.length;
    const cols = boardState[0].length;

    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const index = r * cols + c;
            const cell = grid.children[index];
            const value = boardState[r][c];

            if (!cell) continue;

            if (value === null) {
                cell.textContent = "?";
                cell.className = "cell";
            } else if (value === -1) {
                cell.textContent = "💣";
                cell.className = "cell revealed mine";
            } else if (value === 0) {
                cell.textContent = "";
                cell.className = "cell revealed";
            } else {
                cell.textContent = value;
                cell.className = `cell revealed cell-number-${value}`;
            }
        }
    }
}

// 🔹 Configuración de eventos al cargar el DOM
document.addEventListener("DOMContentLoaded", () => {
    startGame(); // tablero inicial

    const resetBtn = document.getElementById("reset-btn");
    resetBtn.addEventListener("click", async () => {
        try {
            const res = await fetch("/buscaminas/restart/");
            if (!res.ok) throw new Error('Server returned ' + res.status);
            const data = await res.json();
            boardState = data.board;
            drawBoard(boardState.length, boardState[0].length);
            console.log("Juego reiniciado");
            show_dialogue('inicio', 'buscaminas')
        } catch (err) {
            console.error(err);
        }
    });
});
