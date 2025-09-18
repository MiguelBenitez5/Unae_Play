from django.db.models.functions import Random
import time
from django.shortcuts import render, redirect
from .wordle import Wordle
from globals.utils import save_score, is_session_active
from django.http import JsonResponse
from .models import WordleWord

# Create your views here.

def render_page(request):
    if not is_session_active(request):
        redirect('login')
    #se inicializan los valores por defecto    
    init_game(request)
    return render(request, 'wordle/wordle.html')

def play_wordle(request, userword):
    if not is_session_active(request):
        return JsonResponse({'status': 'error', 'message': 'La sesion no esta iniciada'})
    if 'game_data' in request.session.get('wordle',{}):
        wordle = Wordle(request.session['wordle']['game_data'])
        response = wordle.play_game(userword)

        if response['status'] == 'error':
            return JsonResponse(response)
        
        match response['game_status']:
            case 'win' | 'defeat':
                save_score(request,'wordle',response['game_data']['score'])
        
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
            'word': word.word
        },
        'backlist': backlist.append(word.word)
    })