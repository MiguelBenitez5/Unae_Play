const game = document.getElementById('game');
const rows = 8;
const cols = 8;
const minesCount = 10;

let board = [];

// Crear celdas
for (let r = 0; r < rows; r++) {
    board[r] = [];
    for (let c = 0; c < cols; c++) {
        const cell = document.createElement('div');
        cell.classList.add('cell');
        cell.style.width = "30px";
        cell.style.height = "30px";
        cell.style.border = "1px solid black";
        cell.style.textAlign = "center";
        cell.style.cursor = "pointer";
        cell.dataset.row = r;
        cell.dataset.col = c;
        cell.addEventListener("click", revealCell);
        game.appendChild(cell);

        board[r][c] = { element: cell, mine: false, revealed: false };
    }
}

// Colocar minas
let placed = 0;
while (placed < minesCount) {
    const randRow = Math.floor(Math.random() * rows);
    const randCol = Math.floor(Math.random() * cols);
    if (!board[randRow][randCol].mine) {
        board[randRow][randCol].mine = true;
        placed++;
    }
}

// Contar minas alrededor
function countMines(r, c) {
    let count = 0;
    for (let i = -1; i <= 1; i++) {
        for (let j = -1; j <= 1; j++) {
            if (i === 0 && j === 0) continue;
            const newRow = r + i;
            const newCol = c + j;
            if (newRow >= 0 && newRow < rows && newCol >= 0 && newCol < cols) {
                if (board[newRow][newCol].mine) count++;
            }
        }
    }
    return count;
}

// Revelar celda
function revealCell(e) {
    const r = parseInt(e.target.dataset.row);
    const c = parseInt(e.target.dataset.col);
    const cell = board[r][c];
    if (cell.revealed) return;

    cell.revealed = true;
    cell.element.style.background = "#ddd";

    if (cell.mine) {
        cell.element.textContent = "💣";
        alert("Game Over!");
    } else {
        const mines = countMines(r, c);
        if (mines > 0) {
            cell.element.textContent = mines;
        }
    }
}