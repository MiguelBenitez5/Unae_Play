from django.shortcuts import render, redirect
from globals.utils import is_session_active, save_score
import time
from wordle.models import WordleWord
from django.db.models.functions import Random
from django.http import JsonResponse
from .ahorcado import GuessTheWord

# Create your views here.

def render_page(request):
    if not is_session_active(request):
        return redirect('login')
    init_game(request)
    return render(request, 'ahorcado/ahorcado.html')

def play_game(request, userchar:chr):
    if not is_session_active(request):
        return JsonResponse({'status': 'error', 'message':'La sesion no esta iniciada'})
    if 'game_data' in request.session.get('ahorcado'):
        guess_word = GuessTheWord(request.session['ahorcado']['game_data'])

        play_game = guess_word.play_game(userchar)

        if 'status' in play_game:
            if play_game['status'] == 'error':
                return JsonResponse(play_game['message'])
        if 'key_error' in play_game:
            return JsonResponse(play_game)
        
        match play_game.get('game_status'):
            case 'win' | 'defeat':
                play_game['word'] = request.session['ahorcado']['game_data']['word']
                save_score(request, 'ahorcado', play_game['score'])
        
        request.session['ahorcado']['game_data'].update(play_game['game_data'])
        request.session.modified = True

        return JsonResponse(play_game)
    
    return JsonResponse({'status':'error',"message": 'Error desconocidamente desconocido'})


def init_game(request):
    guess_word = request.session.get('ahorcado')
    if not guess_word:
        guess_word = request.session.setdefault('ahorcado')

    guess_word.setdefault('game_data',{
        'start_time'  : time.time(),
        'tries'       : 5,
        'score'       : 0,
        'chars_played': [],
        'amount_words': 0,
        'result'      : {}
    })
    guess_word.setdefault('game_status', 0)

    request.session.modified = True
    #se genera una nueva palabra si no existe en la sesion
    word = None
    if not 'word' in request.session['ahorcado']['game_data']:
        blacklist = list(request.session.get('ahorcado', {}).get('blacklist', []))
        #se obtiene una palabra aleatoria de la base de datos
        word = WordleWord.objects.exclude(word__in=blacklist).order_by(Random()).first()
        if word:
            blacklist.append(word.word)
            request.session['ahorcado']['blacklist'] = blacklist
        else:
            word = WordleWord.objects.order_by(Random()).first()

        request.session['ahorcado']['game_data']['word'] = word.word
        request.session['ahorcado']['game_data']['word_len'] = len(word.word)
        request.session.modified = True
        
        if 'game_status' in request.session['ahorcado']:
            request.session['ahorcado']['game_status'] = 0

        request.session.modified = True
            


def restart_game(request):
    if 'ahorcado' in request.session:
        request.session['ahorcado'].pop('game_data', None)
        request.session.modified = True
        init_game(request)
        return JsonResponse({'status':'success', 'message':'Juego restablecido correctamente'})
    return JsonResponse({'status':'error', 'message':'No se pudo reestablecer el juego D:'})


def get_data(request):
    if 'game_data' in request.session.get('ahorcado'):
        data = request.session.get('ahorcado').get('game_data')
        response = {
            
            'game_data':{
                'status': 'success',
                'tries' : data['tries'],
                'word_len': data['word_len'],
                'score' : data['score'],
                'result' : data['result'],
                'amount_words': data['amount_words'],
                'chars_played': data['chars_played'],
            },
            
        }
        return JsonResponse(response)
    return JsonResponse({'status':'error','message':'No se pudo obtener los datos'})


