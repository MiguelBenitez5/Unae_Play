import time

CORRECT_LETTER = 1000

class GuessTheWord:
    def __init__(self, session_data):
        self.__start_time = session_data['start_time']
        self.__word = session_data['word'].lower()
        self.__tries = session_data['tries']
        self.__score = session_data['score']
        self.__len = session_data['word_len']
        self.__chars_played = session_data['chars_played']
        self.__amount_words = session_data['amount_words']
        self.__result = session_data['result']

    def __get_all_data(self):
        return {
            'tries'       : self.__tries,
            'score'       : self.__score,
            'word_len'    : self.__len,
            'chars_played': self.__chars_played,
            'amount_words': self.__amount_words,
            'result'      : self.__result
        }
    
    def play_game(self, userchar:chr):
        result = self.__compare_char(userchar)
            

        if not result:
            return {'status': 'error','message': 'Solo se puede jugar 1 letra por turno'}
        if result.get('error'):
            return {'key_error': result['error']}
        

        game_data = self.__get_all_data()

        response = {
            'game_data': game_data,
            'status'   : 'success'
        }

        if result.get('not_found'):
            response['not_found'] = result['not_found']

        else:
            self.__result.update(result)

        elapsed_time = time.time() - self.__start_time
        check_result = self.__check_result()
        #calculando puntaje
        match check_result:
            case 'win' | 'defeat':
                score = ((CORRECT_LETTER * self.__amount_words) / elapsed_time)*self.__tries
                if (check_result == 'win'):
                    #si gana se multiplica su score x3
                    score *= 3
                response['game_status'] = check_result
                response['score'] = score
        
        return response

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
    
    def __compare_char(self, userchar:chr):
        word_data = self.__get_word_data()

        if len(userchar) > 1:
            return False

        if userchar in self.__chars_played:
            return {'error': 'Esta letra ya fue jugada'}
        
        if userchar not in word_data:
            self.__chars_played.append(userchar)
            self.__tries -= 1
            return {'not_found' :'Esta letra no se encuentra en la palabra'}
        
        if userchar in word_data:
            self.__chars_played.append(userchar)
            self.__amount_words += word_data[f'{userchar}']['amount']
            response = {}
            for position in word_data[f'{userchar}']['positions']:
                response[f'{position}'] = userchar
            return response 
        

    def __check_result(self):
        if self.__amount_words == len(self.__word):
            return 'win'

        if self.__tries < 1:
            return 'defeat'
        
        return 0
    
