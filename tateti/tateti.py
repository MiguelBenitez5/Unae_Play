import random
#Constantes de la aplicacion:
#para calcular los puntajes se utilizara la formula de CIELO/tiempo donde tiempo se representa en minutos
MAX_WIN = 100000
MAX_DRAW = 50000
MAX_DEFEAT = 20000

MIN_WIN = 1000
MIN_DRAW = 500
MIN_DEFEAT = 200


class Tateti:

    def __init__(self, session_data):
        self.__start_time = session_data['start_time']
        self.__score = session_data['score']
        self.__board = session_data['board']
        self.__level = session_data['level']
        self.__playerMoves = session_data['player_moves']
        self.__machineMoves = session_data['machine_moves']
        self.__draws = session_data['player_draws']


    def __restart_game(self):
        self.__board = [[" " for _ in range(3)] for _ in range(3)]
        self.__playerMoves = 0
        self.__machineMoves = 0

    def __next_level(self):
        match self.__level:
            case 'easy':
                return 'medium'
            case 'medium':
                return 'hard'
        
            

    def play_game(self, row, column):
        machine_move = None
        hard_machine_move = None
        #si la jugada es incorrecta se retorna false
        if not self.__playPlayer(row, column):
            return False
        #se suma un movimiento al jugador
        self.__playerMoves += 1
        #por defecto el estado del juego esta en 0, esto indica que el juego continua
        game_status = 0
        #se comprueba si gano el usuario
        if self.__checkBoard() == 1:
            #calcular puntaje del jugador
            score = MAX_WIN/(self.__start_time/60)
            if score < MIN_WIN:
                score =  MIN_WIN
            self.__score += score
            self.__level = self.__next_level()
            game_status = 'win'
            self.__restart_game()
        
        #se comprueba empate
        elif self.__playerMoves >= 5:
            self.__draws += 1
            if self.__draws >=3:
                game_status = 'defeat'
            else:
                score = MAX_DRAW/(self.__start_time/60)
                if score < MIN_DRAW:
                    score = MIN_DRAW
                self.__score += score
                game_status = 'draw'
            self.__restart_game()
        
        #juega la maquina
        else: 
            machine_move = self.__playMachine()
            self.__machineMoves += 1
            #se comprueba si gana la maquina
            if self.__checkBoard() == -1:
                score = MAX_DEFEAT/(self.__start_time/60)
                if score < MIN_DEFEAT:
                    score = MIN_DEFEAT
                self.__score += score
                game_status = 'defeat'
                self.__restart_game()
            
            #se comprueba empate 
            elif self.__machineMoves >= 5:
                score = MAX_DRAW/(self.__start_time/60)
                if score < MIN_DRAW:
                    score = MIN_DRAW
                self.__score += score
                game_status = 'defeat'
                self.__restart_game()

        #jugada extra en caso de que la maquina sea dificil
        if self.__level == 'hard' and self.__machineMoves == 0:
            self.__machineMoves += 1
            hard_machine_move = self.__playMachine()

        response = {
            'status': 'success',
            'start_time': self.__start_time,
            'board': self.__board,
            'level': self.__level,
            'score': self.__score,
            'player_moves': self.__playerMoves,
            'machine_moves': self.__machineMoves,
            'game_status': game_status,
            'player_draws': self.__draws,
        }
        if machine_move:
            response['machine_move'] = machine_move
        if hard_machine_move:
            response['hard_machine_move'] = hard_machine_move
        
        #retorno de diccionario con el fin de utilizarlo en la sesion y la respues al usuario
        return response

    def __playPlayer(self, row, column):
        """
        Jugada del jugador\n
        Param (row): la fila seleccionada\n
        Param (column): la columna seleccionada\n
        Returna: True en caso de que la jugada fue realizada correctamente y False en caso contrario
        """
        #tener en cuenta la comprobacion de los valores fuera de rango de la lista
        #unicamente se realiza la jugada si la posicion seleccionada aun no fue jugada
        if self.__board[row][column] ==  ' ':
            self.__board[row][column] = 'X'
            return True
        else :
            return False

    
    def __playMachine(self):
        """
        Juega la maquina
        """
        #se suma una jugada a la maquina
        match self.__level:
            case 'easy':
                return self.__machineEasy()
            case 'medium':
                #juega una posicion aleatoria en caso de retornar False
                machinePlay = self.__machineMedium()
                if not machinePlay:
                    return self.__machineEasy()
            case 'hard':
                #primero verifica si puede ganar la maquina o el jugador, si no se cumple juega su plantilla
                machinePlay = self.__machineMedium()
                if not machinePlay: 
                    return self.__machineHard()
    

    def __checkBoard(self):
        """
        Comprobar el tablero.

        Retorna:
        -1 En caso de que la maquina ha ganado
        0 En caso neutral (sigue el juego)
        1 En caso de que ha ganado el jugador
        """
        
        for i in range(3):
            ##Comprobar si gana el jugador##
            #comprobando filas
            if ((self.__board[i][0] == 'X' and self.__board[i][1] == 'X' and self.__board[i][2] == 'X') or
            #comprobando columnas
            (self.__board[0][i] == 'X' and self.__board[1][i] == 'X' and self.__board[2][i] == 'X') or
            #comprobando diagonal principal
            (self.__board[0][0] == 'X' and self.__board[1][1] == 'X' and self.__board[2][2] == 'X') or
            #comprobando diagonal secundaria
            (self.__board[0][2] == 'X' and self.__board[1][1] == 'X' and self.__board[2][0] == 'X')):
                return 1
            
            ##Comprobar si gana la maquina
            #comprobando filas
            if ((self.__board[i][0] == '0' and self.__board[i][1] == '0' and self.__board[i][2] == '0') or
            #comprobando columnas
            (self.__board[0][i] == '0' and self.__board[1][i] == '0' and self.__board[2][i] == '0') or
            #comprobando diagonal principal
            (self.__board[0][0] == '0' and self.__board[1][1] == '0' and self.__board[2][2] == '0') or
            #comprobando diagonal secundaria
            (self.__board[0][2] == '0' and self.__board[1][1] == '0' and self.__board[2][0] == '0')):
                return -1
            
        ##Si no gana ninguno el juego continua##
        return 0
        
    def __restartBoard(self):
        """
        Reiniciar el tablero a los valores iniciales 
        """
        for i in range(3):
            self.__board[i][0] = ' '
            self.__board[i][1] = ' '
            self.__board[i][2] = ' '
        
        return self.__board
    

    def __machineEasy(self):
        """
        La jugada de la maquina en su nivel mas facil, solo juega una posicion aleatoria en cada turno
        """
        while True:
            randomRow = int(random.uniform(0,2))
            randomColumn = int(random.uniform(0,2))
            if self.__board[randomRow][randomColumn] == ' ':
               self.__board[randomRow][randomColumn] = '0'
               return str(randomRow)+'-'+str(randomColumn)

    def __machineMedium(self):
        """
        La jugada de la maquina en nivel medio, es un poco mas inteligente que su version facil, si tiene opcion de victoria la toma y no permite ganar facilmente al jugador\n
        En caso de que ninguno tenga una jugada ganadora, juega posicion aleatoria\n
        Retorna: True si realiza una "jugada inteligente" y False si no
        """
        
        for i in range(3):
            ##Comprobar si la maquina esta a punto de ganar##
            #comprobando filas
            if (self.__board[i][0] == '0' and self.__board[i][1] == '0') or (self.__board[i][2] == '0' and self.__board[i][1] == '0') or (self.__board[i][0] == '0' and self.__board[i][2] == '0'):
                if ' ' in self.__board[i]:
                    index = self.__board[i].index(' ')
                    self.__board[i][index] = '0'
                    return f"{i}-{index}"
            #comprobando columnas
            if (self.__board[0][i] == '0' and self.__board[1][i] == '0') or (self.__board[2][i] == '0' and self.__board[1][i] == '0') or (self.__board[0][i] == '0' and self.__board[2][i] == '0'):
                for f in range(3):    
                    if self.__board[f][i] == ' ':
                        self.__board[f][i] = '0'
                        return f'{f}-{i}'
            #comprobando diagonal principal
            if self.__board[0][0] == '0' and self.__board[1][1] == '0':
                if self.__board[2][2] == ' ':
                    self.__board[2][2] = '0'
                    return '2-2'
            elif self.__board[2][2] == '0' and self.__board[1][1] == '0':
                if self.__board[0][0] == ' ':
                    self.__board[0][0] = '0'
                    return '0-0'
            elif self.__board[0][0] =='0' and self.__board[2][2] == '0':
                if self.__board[1][1] == ' ':
                    self.__board[1][1] = '0'
                    return '1-1'  

            #comprobando diagonal secundaria
            if self.__board[0][2] == '0' and self.__board[2][0] == '0':
                if self.__board[1][1] == ' ':
                    self.__board[1][1] = '0'
                    return '1-1'
            elif self.__board[0][2] == '0' and self.__board[1][1] == '0':
                if self.__board[2][0] == ' ':
                    self.__board[2][0] = '0'
                    return '2-0'
            elif self.__board[2][0] =='0' and self.__board[1][1] == '0':
                if self.__board[0][2] == ' ':
                    self.__board[0][2] = '0'
                    return '0-2'    
            
            ##Comprobar si el jugador esta a punto de ganar##
            #comprobando filas
            if (self.__board[i][0] == 'X' and self.__board[i][1] == 'X') or (self.__board[i][2] == 'X' and self.__board[i][1] == 'X') or (self.__board[i][0] == 'X' and self.__board[i][2] == 'X'):
                if ' ' in self.__board[i]:
                    index = self.__board[i].index(' ')
                    self.__board[i][index] = '0'
                    return True
            #comprobando columnas
            if (self.__board[0][i] == 'X' and self.__board[1][i] == 'X') or (self.__board[2][i] == 'X' and self.__board[1][i] == 'X') or (self.__board[0][i] == 'X' and self.__board[2][i] == 'X'):
                for f in range(3):    
                    if self.__board[f][i] == ' ':
                        self.__board[f][i] = '0'
                        return f'{f}-{i}'
            #comprobando diagonal principal
            if self.__board[0][0] == 'X' and self.__board[1][1] == 'X':
                if self.__board[2][2] == ' ':
                    self.__board[2][2] = '0'
                    return '2-2'
            elif self.__board[2][2] == 'X' and self.__board[1][1] == 'X':
                if self.__board[0][0] == ' ':
                    self.__board[0][0] = '0'
                    return '0-0'
            elif self.__board[0][0] =='X' and self.__board[2][2] == 'X':
                if self.__board[1][1] == ' ':
                    self.__board[1][1] = '0'
                    return '1-1'   

            #comprobando diagonal secundaria
            if self.__board[0][2] == 'X' and self.__board[2][0] == 'X':
                if self.__board[1][1] == ' ':
                    self.__board[1][1] = '0'
                    return '1-1'
            elif self.__board[0][2] == 'X' and self.__board[1][1] == 'X':
                if self.__board[2][0] == ' ':
                    self.__board[2][0] = '0'
                    return '2-0'
            elif self.__board[2][0] =='X' and self.__board[1][1] == 'X':
                if self.__board[0][2] == ' ':
                    self.__board[0][2] = '0'
                    return '0-2'
            
        #si al finalizar el recorrido no se cumple ninguna retorna False
        return False

    def __machineHard(self):
        """
        El modo mas inteligente de la maquina, donde ella empieza el juego y planea estrategias para ganar
        """
        #juega aleatorio si el jugador ha marcado en el centro
        if self.__board[1][1] == 'X':
            return self.__machineEasy()
         
        tries = 0
        while tries < 10 :
            #hacer 10 intentos, aqui creo un numero aleatorio para seleccionar aleatoriamente una jugada
            randomNumber = int(random.uniform(1,8))
            #aplicar la estrategia dependiendo del numero aleatorio generado
            match randomNumber:
                case 1:
                    strat = self.__strategy_1(self.__machineMoves)
                    if strat:
                        return strat
                case 2:
                    strat = self.__strategy_2(self.__machineMoves)
                    if strat:
                        return strat
                case 3:
                    strat = self.__strategy_3(self.__machineMoves)
                    if strat:
                        return strat
                case 4:
                    strat = self.__strategy_4(self.__machineMoves)
                    if strat:
                        return strat
                case 5:
                    strat = self.__strategy_5(self.__machineMoves)
                    if strat:
                        return strat
                case 6:
                    strat = self.__strategy_6(self.__machineMoves)
                    if strat:
                        return strat
                case 7:
                    strat = self.__strategy_7(self.__machineMoves)
                    if strat:
                        return strat
                case 8:
                    strat = self.__strategy_8(self.__machineMoves)
                    if strat:
                        return strat                    
            tries += 1
            #en caso de que no puede aplicar ninguna estrategia luego de 10 intentos, juega aleatorio                 
            if tries >=10:
                return self.__machineEasy() 

    #Varias estrategias para el modo dificil (estan hechas en funciones para mejorar la legibilidad)
    def __strategy_1(self,moves):
        match moves:
            #primer movimiento
            case 1:
                self.__board[0][0] = '0'
                return '0-0'
            #segundo movimiento
            case 2:
                if self.__board[0][2] != 'X' and self.__board[0][0] == '0' and self.__board[0][1] != 'X':
                    self.__board[0][2] = '0'
                    return "0-2"
                else:
                    return False
            #tercer movimiento
            case 3:
                if self.__board[0][0] == '0' and self.__board[0][2] == '0' and self.__board[2][2] != 'X' and self.__board[2][0] != 'X':
                    self.__board[1][1] = '0'
                    return "1-1"
                else:
                    return False


    def __strategy_2(self,moves):
        match moves:
            case 1:
                self.__board[0][2] = '0'
                return "0-2"
            case 2:
                if self.__board[0][0] != 'X' and self.__board[0][2] == '0' and self.__board[0][1] != 'X':
                    self.__board[0][0] = '0'
                    return "0-0"
                else:
                    return False
            case 3:
                if self.__board[0][0] == '0' and self.__board[0][2] == '0' and self.__board[2][2] != 'X' and self.__board[2][0] != 'X':
                    self.__board[1][1] = '0'
                    return "1-1"
                else:
                    return False
                
    def __strategy_3(self,moves):
        match moves:
            case 1:
                self.__board[2][2] = '0'
                return "2-2"
            case 2:
                if self.__board[0][2] != 'X' and self.__board[2][2] == '0' and self.__board[1][2] != 'X':
                    self.__board[0][2] = '0'
                    return "0-2"
                else:
                    return False
            case 3:
                if self.__board[2][2] == '0' and self.__board[0][2] == '0' and self.__board[2][0] != 'X' and self.__board[0][0] != 'X':
                    self.__board[1][1] = '0'
                    return "1-1"
                else:
                    return False
    
    def __strategy_4(self,moves):
        match moves:
            case 1:
                self.__board[2][0] = '0'
                return "2-0"
            case 2:
                if self.__board[0][0] != 'X' and self.__board[2][0] == '0' and self.__board[1][0] != 'X':
                    self.__board[0][0] = '0'
                    return "0-0"
                else:
                    return False
            case 3:
                if self.__board[2][0] == '0' and self.__board[0][0] == '0' and self.__board[0][2] != 'X' and self.__board[2][2] != 'X':
                    self.__board[1][1] = '0'
                    return "1-1"
                else:
                    return False
                
    def __strategy_5(self,moves):
        match moves:
            case 1:
                self.__board[1][1] = '0'
                return "1-1"
            case 2:
                if self.__board[1][1] == '0' and self.__board[0][0] != 'X' and self.__board[0][2] != 'X' and self.__board[2][2] != 'X' and self.__board[2][0] != 'X' and self.__board[0][1] != 'X' and self.__board[2][1] != 'X':
                    self.__board[2][1] = '0'
                    return "2-1"
                else:
                    return False
            case 3:
                if self.__board[2][1] == '0' and self.__board[1][1] == '0' and self.__board[0][0] != 'X' and self.__board[2][0] != 'X':
                    self.__board[2][2] = '0'
                    return "2-2"
                else:
                    return False
                
    def __strategy_6(self,moves):
        match moves:
            case 1:
                self.__board[1][1] = '0'
                return "1-1"
            case 2:
                if self.__board[1][1] == '0' and self.__board[0][0] != 'X' and self.__board[0][2] != 'X' and self.__board[2][2] != 'X' and self.__board[2][0] != 'X' and self.__board[1][0] != 'X' and self.__board[1][2] != 'X':
                    self.__board[1][2] = '0'
                    return "1-2"
                else:
                    return False
            case 3:
                if self.__board[1][2] == '0' and self.__board[1][1] == '0' and self.__board[2][0] != 'X' and self.__board[2][2] != 'X':
                    self.__board[0][2] = '0'
                    return "0-2"
                else:
                    return False
                
    def __strategy_7(self,moves):
        match moves:
            case 1:
                self.__board[1][1] = '0'
                return "1-1"
            case 2:
                if self.__board[1][1] == '0' and self.__board[0][0] != 'X' and self.__board[0][2] != 'X' and self.__board[2][2] != 'X' and self.__board[2][0] != 'X' and self.__board[1][2] != 'X' and self.__board[1][0] != 'X':
                    self.__board[1][0] = '0'
                    return "1-0"
                else:
                    return False
            case 3:
                if self.__board[1][0] == '0' and self.__board[1][1] == '0' and self.__board[0][0] != 'X' and self.__board[0][2] != 'X':
                    self.__board[2][0] = '0'
                    return "2-0"
                else:
                    return False
    
    def __strategy_8(self,moves):
        match moves:
            case 1:
                self.__board[1][1] = '0'
                return "1-1"
            case 2:
                if self.__board[1][1] == '0' and self.__board[0][0] != 'X' and self.__board[0][2] != 'X' and self.__board[2][2] != 'X' and self.__board[2][0] != 'X' and self.__board[0][1] != 'X' and self.__board[2][1] != 'X':
                    self.__board[2][1] = '0'
                    return "2-1"
                else:
                    return False
            case 3:
                if self.__board[0][1] == '0' and self.__board[1][1] == '0' and self.__board[0][2] != 'X' and self.__board[0][0] != 'X':
                    self.__board[2][2] = '0'
                    return "2-2"
                else:
                    return False