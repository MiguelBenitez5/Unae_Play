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
    api_response = requests.get(f'https://rae-api.com/api/words/{userword.lower()}')
    data = api_response.json()
    #consultar la base de datos en busca de existencia de la palabra ingresada
    exists = WordleWord.objects.filter(word__iexact=userword).exists()

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
        
        #guardar datos en sesion
        request.session['wordle']['game_data'].update(response['game_data'])

        #guardar la respuespta en sesion
        request.session.setdefault('wordle', {}).setdefault('history',{})
        request.session['wordle']['history'][f'{response['game_data']['tries']}'] = response

        #para probar, borrar luego
        print(request.session['wordle']['history'])
        request.session.modified = True
        
        return JsonResponse(response)
    
    return JsonResponse({"status": "error", "message": "No existen datos de juego D:"})



def reset_game(request):
    if 'wordle' in request.session:
        request.session['wordle'].pop('game_data', None)
        request.session['wordle'].pop('history', None)
        request.session.modified = True
        init_game(request)
        return JsonResponse({'status':'success', 'message':'Juego restablecido correctamente'})
    return JsonResponse({'status':'error', 'message':'No se pudo reestablecer el juego D:'})
    

def init_game(request):
    #se genera una nueva palabra si no existe en la sesion
    word = None
    if not request.session.get('wordle',{}).get('game_data', {}):
        print("Estoy aqui god")
        blacklist = list(request.session.get('wordle', {}).get('blacklist', []))
        #se obtiene una palabra aleatoria de la base de datos
        word = WordleWord.objects.exclude(word__in=blacklist).order_by(Random()).first()
        if 'wordle' in request.session:
            if word:
                blacklist.append(word.word)
                request.session['wordle']['blacklist'] = blacklist
                request.session.modified = True
            else:
                word = WordleWord.objects.order_by(Random()).first()
        #se crea la palabra al ingresar a la pagina
        wordle = request.session.setdefault('wordle',{'blacklist': blacklist})
        wordle.setdefault('game_data', {
                'start_time': time.time(),
                'tries': 0,
                'word' : word.word,
                'word_len'  : len(word.word),
            })
        wordle.setdefault('game_status', 0)
        request.session.modified = True


def get_initial_data(request):
    request.session.setdefault('wordle',{}).setdefault('game_data', {'tries': 0, 'word_len': 0})
    history = request.session['wordle'].get('history', None)
    response = {'basic_data': {
                    'tries': request.session['wordle']['game_data']['tries'],
                    'word_len': request.session['wordle']['game_data']['word_len']
                    },
                 'history': history
                }
    print(f'Datos basicos: {response}')
    
    return JsonResponse(response)