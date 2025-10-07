import random

class Minesweeper:
    def __init__(self, rows=10, cols=10, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self._place_mines()
        self._calculate_numbers()
    
    def _place_mines(self):
        count = 0
        while count < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.board[r][c] == -1:
                continue
            self.board[r][c] = -1  # mina
            count += 1

    def _calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                mines_count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.board[nr][nc] == -1:
                                mines_count += 1
                self.board[r][c] = mines_count

    def reveal(self, r, c):
        """Revelar solo la celda seleccionada"""
        if self.revealed[r][c]:
            return
        self.revealed[r][c] = True


    def is_mine(self, r, c):
        return self.board[r][c] == -1

    def is_finished(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.revealed[r][c] and self.board[r][c] != -1:
                    return False
        return True
