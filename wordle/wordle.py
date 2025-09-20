import time

GREEN_CHAR = 10000
YELLOW_CHAR = 3000
WIN_POINTS = 5
DEFEAT_POINTS = 1


class Wordle:

    def __init__(self, session_data):
        self.__start_time = session_data['start_time']
        self.__word = session_data['word']
        self.__tries = session_data['tries']
        self.__score = 0
        self.__len = session_data['word_len']
    
    """
    Se realiza y analiza la jugada\n
    Retorna: un diccionario con todos los datos necesarios para el sistema\n
    Complejidad: O(n) 
    """
    def play_game(self, userword):
        result = self.__compare_words(userword) #metodo con complejidad O(n)
        if not result:
            return {
                'status' : 'error',
                'message': 'La longitud del texto es superior o inferior de lo esperado'
            }
        
        self.__tries += 1

        response={
            'status'     : 'success',
            'result'     : result,
            'game_data'  : {
                           'tries' : self.__tries ,
                           'score' : self.__score,
                           },
        }
        user_win = False
        if userword == self.__word:
            response['game_status'] = 'win'
            response['game_data']['score'] = self.__calculate_final_score()* WIN_POINTS
            user_win = True    
        if self.__tries > 6 and not user_win:
            response['game_status'] = 'defeat'
            response['game_data']['score'] = self.__calculate_final_score()* DEFEAT_POINTS
        return response

    """
    Se crea un diccionario con los datos necesarios de la palabra que debe ser adivinada\n
    Su complejidad es O(n), ya que siempre recorrera todas las letras de la palabra de principio a fin
    Retorna: el diccionario con los datos
    """
    def __get_word_data(self):
        word_data = {}
        for i, char in enumerate(self.__word):
            if not char in word_data:
                word_data[f'{char}'] = {'positions': [i],
                                         'amount'  : 1
                                      }
            else:
                word_data[f'{char}']['positions'].append(i)
                word_data[f'{char}']['amount'] += 1
        
        return word_data
    
    """
    Calcula el puntaje de acuerdo al nivel de certeza 
    Complejidad O(1) :D
    """
    def __calculate_score(self, color):
        match color:
            case 'green':
                self.__score += GREEN_CHAR
            case 'yellow':
                self.__score += YELLOW_CHAR
    
    def __calculate_final_score(self):
        #formula: (Puntaje/tiempo)/intentos
        current_time = time.time()/60
        elapsed_time = current_time - (self.__start_time/60) 
        return int((self.__score/elapsed_time)/self.__tries)

    """
    Se compara la palabra generada con la ingresada por el usuario\n
    Tambien se calcula la suma de puntajes por cada letra verde y amarilla\n
    Retorna: un diccionario con el color correspondiente en cada indice
    Complejidad: O(n)
    """
    def __compare_words(self, userword):
        #se compara longitud para evitar errores en el recorrido del bucle
        if len(userword) != self.__len:
            return False
        
        word_generated = self.__get_word_data()
        result = {}

        for i, char in enumerate(userword):
            #si el caracter no se encuentra en el diccionario es gris
            if char not in word_generated:
                result[f'{i}'] = {'color':'grey','char': char}
            #si el indice actual se encuentra entre las posiciones del caracter es verde
            #el puntaje calculado es de correspondiente a letra verde
            elif i in word_generated[f'{char}']['positions']:
                result[f'{i}'] = {'color':'green','char': char}
                word_generated[f'{char}']['amount'] -= 1
                self.__calculate_score('green')
            #si existe la letra en diferente posicion y cantidad adecuada es amarilla
            #el puntaje calculado es de correspondiente a letra amarilla
            elif word_generated[f'{char}']['amount'] > 0 and i not in word_generated[f'{char}']['positions']:
                result[f'{i}'] = {'color':'yellow','char': char}
                word_generated[f'{char}']['amount'] -= 1
                self.__calculate_score('yellow')
            #si se supera la cantidad maxima de letras
            else:
                result[f'{i}'] = {'color':'grey','char': char}
        #al finalizar se retorna el diccionario con los datos
        return result
    

    
            

