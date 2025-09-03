import time
import random

class Tateti:

    def __init__(self, board,playerMoves,machineMoves, level):
        self.__board = board
        self.__level = level
        self.__playerMoves = playerMoves
        self.__machineMoves = machineMoves

    def getBoard(self):
        """
        Se obtiene el tablero actual del objeto\n
        Retorna: un array bidimensional con los valores del tablero 

        """
        return self.__board
    
    def getLevel(self):
        """
        Se obtiene el nivel de dificultad actual

        Retorna: el nivel de difucultad
        """
        return self.__level
    
    def setLevel(self, level):
        """
        Cambia el nivel de dificultad
        Param(level): el nivel de dificultad deseado (easy,medium,hard)
        """
        self.__level = level
    
    def playPlayer(self, row, column):
        """
        Jugada del jugador\n
        Param (row): la fila seleccionada\n
        Param (column): la columna seleccionada\n
        Returna: True en caso de que la jugada fue realizada correctamente y False en caso contrario
        """
        #unicamente se realiza la jugada si la posicion seleccionada aun no fue jugada
        if self.__board[row][column] is  ' ':
            self.__board = 'X'
            self.__playerMoves += 1
            return True
        else :
            return False

    
    def playMachine(self):
        """
        Juega la maquina
        """
        #se suma una jugada a la maquina
        self.__machineMoves += 1
        match self.__level:
            case 'easy':
                return self.__machineEasy()
            case 'mediun':
                #juega una posicion aleatoria en caso de retornar False
                machinePlay = self.__machineMedium()
                if not machinePlay:
                    return self.__machineEasy()
            case 'hard':
                #primero verifica si puede ganar la maquina o el jugador, si no se cumple juega su plantilla
                machinePlay = self.__machineMedium()
                if not machinePlay: 
                    return self.__machineHard()
    

    def checkBoard(self):
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
            if ((self.__board[i][0] == 'X' and self._board[i][1] == 'X' and self._board[i][2] == 'X') or
            #comprobando columnas
            (self.__board[0][i] == 'X' and self._board[1][i] == 'X' and self._board[2][i] == 'X') or
            #comprobando diagonal principal
            (self.__board[0][0] == 'X' and self._board[1][1] == 'X' and self._board[2][2] == 'X') or
            #comprobando diagonal secundaria
            (self.__board[0][2] == 'X' and self._board[1][1] == 'X' and self._board[2][0] == 'X')):
                return 1
            
            ##Comprobar si gana la maquina
            #comprobando filas
            if ((self.__board[i][0] == '0' and self._board[i][1] == '0' and self._board[i][2] == '0') or
            #comprobando columnas
            (self.__board[0][i] == '0' and self._board[1][i] == '0' and self._board[2][i] == '0') or
            #comprobando diagonal principal
            (self.__board[0][0] == '0' and self._board[1][1] == '0' and self._board[2][2] == '0') or
            #comprobando diagonal secundaria
            (self.__board[0][2] == '0' and self._board[1][1] == '0' and self._board[2][0] == '0')):
                return -1
            
            ##Si no gana ninguno el juego continua##
            return 0
        
    def restartBoard(self):
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
               return [randomRow, randomColumn]

    def __machineMedium(self):
        """
        La jugada de la maquina en nivel medio, es un poco mas inteligente que su version facil, si tiene opcion de victoria la toma y no permite ganar facilmente al jugador\n
        En caso de que ninguno tenga una jugada ganadora, juega posicion aleatoria\n
        Retorna: True si realiza una "jugada inteligente" y False si no
        """
        
        for i in range(3):
            ##Comprobar si la maquina esta a punto de ganar##
            #comprobando filas
            if (self.__board[i][0] == '0' and self._board[i][1] == '0') or (self._board[i][2] == '0' and self._board[i][1] == '0') or (self._board[i][0] == '0' and self._board[i][2] == '0'):
                if ' ' in self.__board[i]:
                    index = self.__board[i].index(' ')
                    self.__board[i][index] = '0'
                    return i+'-'+index
            #comprobando columnas
            if (self.__board[0][i] == '0' and self._board[1][i] == '0') or (self._board[2][i] == '0' and self._board[1][i] == '0') or (self._board[0][i] == '0' and self._board[2][i] == '0'):
                for f in range(3):    
                    if self.__board[f][i] == ' ':
                        self.__board[f][i] = '0'
                        return f+'-'+i
            #comprobando diagonal principal
            if self.__board[0][0] == '0' and self._board[1][1] == '0':
                if self.__board[2][2] == ' ':
                    self.__board[2][2] = '0'
                    return 2+'-'+2
            elif self._board[2][2] == '0' and self.__board[1][1] == '0':
                if self.__board[0][0] == ' ':
                    self.__board[0][0] = '0'
                    return 0+'-'+0
            elif self.__board[0][0] =='0' and self.__board[2][2] == '0':
                if self.__board[1][1] == ' ':
                    self.__board[1][1] = '0'
                    return 1+'-'+1  

            #comprobando diagonal secundaria
            if self.__board[0][2] == '0' and self._board[2][0] == '0':
                if self.__board[1][1] == ' ':
                    self.__board[1][1] = '0'
                    return 1+'-'+1
            elif self._board[0][2] == '0' and self.__board[1][1] == '0':
                if self.__board[2][0] == ' ':
                    self.__board[2][0] = '0'
                    return 2+'-'+0
            elif self.__board[2][0] =='0' and self.__board[1][1] == '0':
                if self.__board[0][2] == ' ':
                    self.__board[0][2] = '0'
                    return 0+'-'+2    
            
            ##Comprobar si el jugador esta a punto de ganar##
            #comprobando filas
            if (self.__board[i][0] == 'X' and self._board[i][1] == 'X') or (self._board[i][2] == 'X' and self._board[i][1] == 'X') or (self._board[i][0] == 'X' and self._board[i][2] == 'X'):
                if ' ' in self.__board[i]:
                    index = self.__board[i].index(' ')
                    self.__board[i][index] = '0'
                    return True
            #comprobando columnas
            if (self.__board[0][i] == 'X' and self._board[1][i] == 'X') or (self._board[2][i] == 'X' and self._board[1][i] == 'X') or (self._board[0][i] == 'X' and self._board[2][i] == 'X'):
                for f in range(3):    
                    if self.__board[f][i] == ' ':
                        self.__board[f][i] = '0'
                        return f+'-'+i
            #comprobando diagonal principal
            if self.__board[0][0] == 'X' and self._board[1][1] == 'X':
                if self.__board[2][2] == ' ':
                    self.__board[2][2] = '0'
                    return 2+'-'+2
            elif self._board[2][2] == 'X' and self.__board[1][1] == 'X':
                if self.__board[0][0] == ' ':
                    self.__board[0][0] = '0'
                    return 0+'-'+0
            elif self.__board[0][0] =='X' and self.__board[2][2] == 'X':
                if self.__board[1][1] == ' ':
                    self.__board[1][1] = '0'
                    return 1+'-'+1   

            #comprobando diagonal secundaria
            if self.__board[0][2] == 'X' and self._board[2][0] == 'X':
                if self.__board[1][1] == ' ':
                    self.__board[1][1] = '0'
                    return 1+'-'+1
            elif self._board[0][2] == 'X' and self.__board[1][1] == 'X':
                if self.__board[2][0] == ' ':
                    self.__board[2][0] = '0'
                    return 2+'-'+0
            elif self.__board[2][0] =='X' and self.__board[1][1] == 'X':
                if self.__board[0][2] == ' ':
                    self.__board[0][2] = '0'
                    return 0+'-'+2
            
        #si al finalizar el recorrido no se cumple ninguna retorna False
        return False

    def __machineHard(self):
        """
        El modo mas inteligente de la maquina, donde ella empieza el juego y planea estrategias para ganar
        """
        #juega aleatorio si el jugador ha marcado en el centro
        if self.__board[1][1] is 'X':
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
                if self.__board[0][2] is not 'X' and self.__board[0][0] is '0' and self.__board[0][1] is not 'X':
                    self.__board[0][2] = '0'
                    return "0-2"
                else:
                    return False
            #tercer movimiento
            case 3:
                if self.__board[0][0] is '0' and self.__board[0][2] is '0' and self.__board[2][2] is not 'X' and self.__board[2][0] is not 'X':
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
                if self.__board[0][0] is not 'X' and self.__board[0][2] is '0' and self.__board[0][1] is not 'X':
                    self.__board[0][0] = '0'
                    return "0-0"
                else:
                    return False
            case 3:
                if self.__board[0][0] is '0' and self.__board[0][2] is '0' and self.__board[2][2] is not 'X' and self.__board[2][0] is not 'X':
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
                if self.__board[0][2] is not 'X' and self.__board[2][2] is '0' and self.__board[1][2] is not 'X':
                    self.__board[0][2] = '0'
                    return "0-2"
                else:
                    return False
            case 3:
                if self.__board[2][2] is '0' and self.__board[0][2] is '0' and self.__board[2][0] is not 'X' and self.__board[0][0] is not 'X':
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
                if self.__board[0][0] is not 'X' and self.__board[2][0] is '0' and self.__board[1][0] is not 'X':
                    self.__board[0][0] = '0'
                    return "0-0"
                else:
                    return False
            case 3:
                if self.__board[2][0] is '0' and self.__board[0][0] is '0' and self.__board[0][2] is not 'X' and self.__board[2][2] is not 'X':
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
                if self.__board[1][1] is '0' and self.__board[0][0] is not 'X' and self.__board[0][2] is not 'X' and self.__board[2][2] is not 'X' and self.__board[2][0] is not 'X' and self.__board[0][1] is not 'X' and self.__board[2][1] is not 'X':
                    self.__board[2][1] = '0'
                    return "2-1"
                else:
                    return False
            case 3:
                if self.__board[2][1] is '0' and self.__board[1][1] is '0' and self.__board[0][0] is not 'X' and self.__board[2][0] is not 'X':
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
                if self.__board[1][1] is '0' and self.__board[0][0] is not 'X' and self.__board[0][2] is not 'X' and self.__board[2][2] is not 'X' and self.__board[2][0] is not 'X' and self.__board[1][0] is not 'X' and self.__board[1][2] is not 'X':
                    self.__board[1][2] = '0'
                    return "1-2"
                else:
                    return False
            case 3:
                if self.__board[1][2] is '0' and self.__board[1][1] is '0' and self.__board[2][0] is not 'X' and self.__board[2][2] is not 'X':
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
                if self.__board[1][1] is '0' and self.__board[0][0] is not 'X' and self.__board[0][2] is not 'X' and self.__board[2][2] is not 'X' and self.__board[2][0] is not 'X' and self.__board[1][2] is not 'X' and self.__board[1][0] is not 'X':
                    self.__board[1][0] = '0'
                    return "1-0"
                else:
                    return False
            case 3:
                if self.__board[1][0] is '0' and self.__board[1][1] is '0' and self.__board[0][0] is not 'X' and self.__board[0][2] is not 'X':
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
                if self.__board[1][1] is '0' and self.__board[0][0] is not 'X' and self.__board[0][2] is not 'X' and self.__board[2][2] is not 'X' and self.__board[2][0] is not 'X' and self.__board[0][1] is not 'X' and self.__board[2][1] is not 'X':
                    self.__board[2][1] = '0'
                    return "2-1"
                else:
                    return False
            case 3:
                if self.__board[0][1] is '0' and self.__board[1][1] is '0' and self.__board[0][2] is not 'X' and self.__board[0][0] is not 'X':
                    self.__board[2][2] = '0'
                    return "2-2"
                else:
                    return False