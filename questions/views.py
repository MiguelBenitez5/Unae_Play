from django.shortcuts import render, redirect
from .questions import QuestionsGame
from globals.utils import is_session_active, save_score
from django.http import JsonResponse
import time

# Create your views here.

def render_page(request):
    if not is_session_active(request):
        return redirect('login')
    restart_game(request)
    return redirect(request, 'questions/questions.html')




def restart_game(request):
    request.session.pop('questions', None)


def request_question(request):
    request.session.setdefault('questions',{
        'start_time'    : time.time(),
        'question'      : None,
        'correct_answer': None,
        'hits'          : 0,
        'level'         : 'easy',
        'score'         : 0,
        'question_info' : None,
        'tries'         : 0,
        'percent'       : 0,
        'backlist'      : []
    })
    sessiondata = request.session.get('questions')
    if sessiondata:
        questions = QuestionsGame(sessiondata)
        response = questions.new_question(request.session['questions']['blacklist'])
        request.session['blacklist'] = response['blacklist']
        questions_data = questions.get_data()
        request.session['questions'].update(questions_data)
        request.session.modified = True

        return JsonResponse(response)
    
    return JsonResponse({
            'status' : 'error',
            'message': 'Ocurrio un error muy lamentable D:'
    })


def answer_question(request, answer):
    sessiondata = request.session.get('questions')
    if not sessiondata:
        return JsonResponse({
            'status' : 'error',
            'message': 'No existen datos de sesion del juego'
        })

    questions = QuestionsGame(sessiondata)
    response = questions.play_game(answer)
    questions_data = questions.get_data()
    request.session['questions'].update(questions_data)
    request.session.modified = True

    if 'game_status' in response:
        if response['game_status'] == 'end':
            save_score(request, 'questions', response['score'])
            if response['percent'] >= 60:
                response['game_status'] = 'win'
            else:
                response['game_status'] = 'defeat'
    

    return JsonResponse(response)
