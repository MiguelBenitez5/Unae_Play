import random
import time

PAIR_POINTS = 50

class MemoryGame:

    def __init__(self, sessiondata):
        self.__start_time = sessiondata['start_time']
        self.__board = sessiondata['board']
        self.__user_choose_1 = sessiondata['user_choose_1']
        self.__user_choose_2 = sessiondata['user_choose_2']
        self.__pairs = sessiondata['pairs']
        self.__score = sessiondata['score']
        self.__position_1 = sessiondata['position_1']
        self.__position_2 = sessiondata['position_2']
        self.__tries = sessiondata['tries']


    def __get_data(self):
        return {
            'board': self.__board,
            'pairs': self.__pairs,
            'score': self.__score,
            'tries': self.__tries
        }

    def __init_board(self):
        start_time = time.time()
        self.__board = [[' ' for _ in range(4)] for _ in range(4)]
        values = 'aabbccddeeffgghh'
        positions = []
        for char in values:
            random_position = f'{random.randint(0,3)}-{random.randint(0,3)}'
            while random_position in positions:
                random_position = f'{random.randint(0,3)}-{random.randint(0,3)}'
            positions.append(random_position)
            row = int(random_position[0])
            col = int(random_position[2])
            self.__board[row][col] = char
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Tiempo de generacion de matriz en segundos: {elapsed_time}")
    
    def play_game(self, row, col):
        if not self.__board:
            self.__init_board()
        
        if row > 3 or col > 3 or row < 0 or col < 0:
            return False
        
        self.__tries += 1
        result = 'not_pair'
        self.__position_1, self.__position_2 = None, None
        user_choice_1, user_choice_2 = None, None
        
        if not self.__user_choose_1:
            self.__user_choose_1 = self.__board[row][col]
            self.__position_1 = f'{row}-{col}'
        else:
            self.__user_choose_2 = self.__board[row][col]
            position_2 = f'{row}-{col}'
            if self.__user_choose_1 == self.__user_choose_2:
                result = 'pair'
                self.__pairs += 1
                self.__score += PAIR_POINTS
            #guardar las referencias
            user_choice_1 = self.__user_choose_1
            user_choice_2 = self.__user_choose_2
            self.__user_choose_1 = None
            self.__user_choose_2 = None

        response = self.__get_data()
        response['result'] = result
        if self.__position_1:
            response['position_1'] = self.__position_1
        response['position_2'] = self.__position_2
        response['user_choose_1'] = self.__user_choose_1
        response['user_choose_2'] = self.__user_choose_2
        response['user_choice_1'] = user_choice_1
        response['user_choice_2'] = user_choice_2
        #Formula para calular puntaje = (Suma de puntajes por cada par * pares acertados) - tiempo*intentos
        if self.__pairs >= 8:
            end_time = time.time()
            elapsed_time = end_time - self.__start_time
            self.__score = (self.__score * self.__pairs) - (int(elapsed_time)*self.__tries)
            response['game_status'] = 'win'
        
        return response

