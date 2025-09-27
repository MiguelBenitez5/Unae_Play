let boardState = [];

async function startGame(rows = 8, cols = 8) {
    drawBoard(rows, cols); // limpiar y dibujar tablero
    try {
        const response = await fetch('/buscaminas/start/');
        if (!response.ok) throw new Error('Server returned ' + response.status);
        const data = await response.json();
        console.log('Game started:', data);
        boardState = data.board || boardState;
        updateBoard();
    } catch (err) {
        console.error(err);
    }
}

async function reveal(r, c) {
    try {
        const response = await fetch(`/buscaminas/reveal/${r}/${c}/`);
        if (!response.ok) throw new Error('Server returned ' + response.status);
        const data = await response.json();
        console.log(data);

        boardState = data.board;
        updateBoard();

        if (data.result === "game_over") {
            setTimeout(() => startGame(boardState.length, boardState[0].length), 2000);
        } else if (data.result === "win") {
            setTimeout(() => startGame(boardState.length, boardState[0].length), 1500);
        }
    } catch (err) {
        console.error(err);
    }
}

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

function updateBoard() {
    const grid = document.getElementById("grid");
    const rows = boardState.length;
    const cols = boardState[0].length;

    // Función recursiva para revelar celdas vacías
    function revealCell(r, c) {
        if (r < 0 || r >= rows || c < 0 || c >= cols) return;
        const index = r * cols + c;
        const cell = grid.children[index];
        const value = boardState[r][c];

        if (!cell || cell.classList.contains('revealed') || value === null) return;

        cell.classList.add('revealed');
        cell.style.transform = 'scale(0)';
        setTimeout(() => cell.style.transform = 'scale(1)', 50);

        if (value === -1) {
            cell.classList.add('mine');
            cell.textContent = "💣";
        } else if (value > 0) {
            cell.textContent = value;
            cell.classList.add(`cell-number-${value}`);
        } else {
            cell.textContent = ""; // celda vacía
            // Si la celda es 0, revelar todas las adyacentes
            for (let dr = -1; dr <= 1; dr++) {
                for (let dc = -1; dc <= 1; dc++) {
                    if (dr !== 0 || dc !== 0) revealCell(r + dr, c + dc);
                }
            }
        }
    }

    // Recorremos todo el board
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const value = boardState[r][c];
            if (value !== null) revealCell(r, c);
        }
    }
}

// Inicializa juego cuando el DOM está listo
document.addEventListener("DOMContentLoaded", () => startGame());
