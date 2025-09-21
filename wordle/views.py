from django.db.models.functions import Random
import time
from django.shortcuts import render, redirect
from .wordle import Wordle
from globals.utils import save_score, is_session_active, correct_word
from django.http import JsonResponse
from .models import WordleWord
import requests

# Create your views here.

def render_page(request):
    if not is_session_active(request):
        return redirect('login')
    #se inicializan los valores por defecto    
    init_game(request)
    return render(request, 'wordle/wordle.html')

def play_wordle(request, userword):
    if not is_session_active(request):
        return JsonResponse({'status': 'error', 'message': 'La sesion no esta iniciada'})
    #consultar si la palabra ingresada por el usuario es una palabra valida del diccionario español
    corrected_word = correct_word(userword)
    api_response = requests.get(f'https://rae-api.com/api/words/{corrected_word}')
    data = api_response.json()
    #consultar la base de datos en busca de existencia de la palabra ingresada
    exists = WordleWord.objects.filter(word__iexact=userword).exists()
    if data:
        if 'error' in data and not exists:
            return JsonResponse({"status": "not_found"})
        

    if 'game_data' in request.session.get('wordle',{}):
        wordle = Wordle(request.session['wordle']['game_data'])
        response = wordle.play_game(userword)

        if response['status'] == 'error':
            return JsonResponse(response)
        
        match response['game_status']:
            case 'win' | 'defeat':
                save_score(request,'wordle',response['game_data']['score'])
        
        #guardar la respuespta en sesion
        wordle = request.session.setdefault('wordle',{})
        history = wordle.session.setdefault('history',{})
        history[f'{response['game_data']['tries']}'] = response
        

        #para probar, borrar luego
        print(history)
        request.session.modified = True
        
        return JsonResponse(response)
    
    return JsonResponse({"status": "error", "message": "No existen datos de juego D:"})



def reset_game(request):
    if 'wordle' in request.session:
        request.session['wordle'].pop('game_data', None)
        request.session.modified = True
        init_game(request)
        return JsonResponse({'status':'success', 'message':'Juego restablecido correctamente'})
    return JsonResponse({'status':'error', 'message':'No se pudo reestablecer el juego D:'})
    

def init_game(request):
    #se genera una nueva palabra si no existe en la sesion
    word = None
    if not request.session.get('wordle',{}).get('game_data', {}):
        backlist = list(request.session.get('wordle', {}).get('blacklist', []))
        #se obtiene una palabra aleatoria de la base de datos
        word = WordleWord.objects.exclude(word__in = backlist).order_by(Random()).first()
        if 'wordle' in request.session:
            request.session['wordle']['blacklist'].append(word.word)
            request.session.modified = True
        #se crea la palabra al ingresar a la pagina
        request.session.setdefault('wordle', {
            'game_data': {
                'start_time': time.time(),
                'tries': 0,
                'word' : word.word,
                'word_len'  : len(word.word),
            },
            'backlist': backlist.append(word.word),
            'game_status': 0
        })

def get_initial_data(request):
    request.session.setdefault('wordle',{'game_data': {'tries': 0, 'word_len': 0}, 'history': None})
    history = request.session.get('history', None)
    response = {'basic_data': {
                    'tries': request.session['wordle']['game_data']['tries'],
                    'word_len': request.session['wordle']['game_data']['word_len']
                    },
                 'history': history
                }
    
    return JsonResponse(response)