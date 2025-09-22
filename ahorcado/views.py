from django.shortcuts import render, redirect
from globals.utils import is_session_active
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
        guess_word = GuessTheWord(request.session['ahoracado']['game_data'])

        play_game = guess_word.play_game(userchar)

        if play_game['status'] == 'error':
            return JsonResponse(play_game['message'])
        if 'key_error' in play_game:
            return JsonResponse(play_game['key_error'])
        


def init_game(request):
    #se genera una nueva palabra si no existe en la sesion
    word = None
    if not request.session.get('ahorcado',{}).get('game_data', {}):
        print("Estoy aqui god")
        blacklist = list(request.session.get('ahorcado', {}).get('blacklist', []))
        #se obtiene una palabra aleatoria de la base de datos
        word = WordleWord.objects.exclude(word__in=blacklist).order_by(Random()).first()
        if 'ahoracado' in request.session:
            if word:
                blacklist.append(word.word)
                request.session['ahoracado']['blacklist'] = blacklist
                request.session.modified = True
            else:
                word = WordleWord.objects.order_by(Random()).first()
        #se crea la palabra al ingresar a la pagina
        guess_word = request.session.setdefault('ahorcado',{'blacklist': blacklist})
        guess_word.setdefault('game_data', {
                'start_time'  : time.time(),
                'tries'       : 5,
                'word'        : word.word,
                'word_len'    : len(word.word),
                'score'       : 0,
                'chars_played': 0,
                'amount_words': 0
            })
        if 'game_status' in request.session['ahorcado']:
            request.session['ahorcado']['game_status'] = 0

        request.session.modified = True
            


def restart_game(request):
    if 'ahoracado' in request.session:
        request.session['ahorcado'].pop('game_data', None)
        request.session.modified = True
        init_game(request)
        return JsonResponse({'status':'success', 'message':'Juego restablecido correctamente'})
    return JsonResponse({'status':'error', 'message':'No se pudo reestablecer el juego D:'})


def get_data(request):
    if 'game_data' in request.session.get('ahoracado'):
        return JsonResponse(request.session['ahorcado']['game_data'])
    return JsonResponse({'status':'error','message':'No se pudo obtener los datos'})
