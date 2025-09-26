from .models import Questions
from django.db.models.functions import Random
import random, time

CORRECT_ANSWER = 50

class QuestionsGame:

    def __init__(self, sessiondata):
        self.__start_time = sessiondata['start_time']
        self.__question = sessiondata['question']
        self.__correct_answer = sessiondata['correct_answer']
        self.__hits = sessiondata['hits']
        self.__level = sessiondata['level']
        self.__score = sessiondata['score']
        self.__question_info = sessiondata['question_info']
        self.__tries = sessiondata['tries']
        self.__persent = sessiondata['percent']

    def get_data(self):
        return {
            'start_time': self.__start_time,
            'question': self.__question,
            'correct_answer': self.__correct_answer,
            'hits' : self.__hits,
            'level': self.__level,
            'score': self.__score,
            'question_info': self.__question_info,
            'tries': self.__tries 
        }


    
    def new_question(self, blacklist:list)-> dict:
        self.__start_time = time.time()
        if not self.__question:
            question = Questions.objects.exclude(id__in=blacklist).order_by(Random()).first()
            if not question:
                return {'status': 'error','message': 'Ocurrio un error en la lectura de la base de datos'}
            blacklist.append(question.id)
            self.__correct_answer = question.correct_answer
            self.__question_info = question.question_info
            answer_list = [self.correct_answer, question.false_answer_1, question.false_answer_2, question.false_answer_3]
            random.shuffle(answer_list)
            answers_random_order = {}
            #se obtiene un diccionario en orden aleatorio con las posiciones de las respuestas
            for i, answer in enumerate(answer_list):
                answers_random_order[f'{i}'] = answer
            return {
                'question' : question.question,
                'answers'  : answers_random_order,
                'blacklist': blacklist
            }
    


    def play_game(self, answer):
        current_time = time.time()
        elapsed_time = int(current_time - self.__start_time)
        response = {}
        if not self.__correct_answer:
            return {'status':'error','message':'Ha ocurrido un error, no hay pregunta'}
        if answer == self.__correct_answer:
            response['status'] = 'correct'
            self.__hits += 1
            self.__score = (self.__score + CORRECT_ANSWER) - elapsed_time 
        else:
            response['status'] = 'incorrect'
            response['correct_option'] = self.__correct_answer
        
        self.__tries += 1
        self.__persent = (self.__hits * 100) // 15
        self.__calculate_score()

        response['percent'] = self.__persent
        response['level'] = self.__level
        response['questio_info'] = self.__question_info
        response['score'] = self.__score

        match self.__level:
            case 'easy':
                if self.__tries >= 5:
                    self.__level = 'medium'
            case 'medium':
                if self.__tries >= 10:
                    self.__level = 'hard'
            case 'hard':
                if self.__tries >= 15:
                    response['game_status'] = 'end'
                    self.__factory_reset()
                    
        self.__question = None
        
        return response

    

    def __factory_reset(self):
        self.__start_time = None
        self.__question = None
        self.__correct_answer = None
        self.__hits = 0
        self.__level = 'easy'
        self.__score = 0
        self.__question_info = None
        self.__tries = 0
        self.__persent = 0

    def __calculate_score(self):
        current_time = time.time()
        elapsed_time = int(current_time - self.__start_time)
        if self.__tries >= 15:
            if self.__persent >= 60:
                self.__score = (self.__score  - elapsed_time) * 5
        

