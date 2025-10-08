# app/adivinarnumero/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .adivinarnumero import AdivinarNumero
from globals.utils import save_score, is_session_active, calculate_score
from globals.constants import NUM_ATTEMPTS, NUM_WIN, NUM_LOSS

import time

def renderPage(request):
    if not is_session_active(request):
        return redirect('login')
    return render(request, 'adivinarnumero/adivinarnumero.html')

def play(request, number):
    try:
        if not is_session_active(request):
            return JsonResponse({'status': 'error', 'message': 'Sesión no iniciada'}, status=403)

        # Recupera o inicializa los datos de la sesión
        request.session.setdefault('adivina', {
            'attempts': 0,
            'score': 0,
            'start_time': time.time(),
        })
        game_data = request.session['adivina']
        game = AdivinarNumero(game_data)
        result = game.guess(number)

        # Si el juego terminó (acertó o perdió)
        if result.get('finished'):
            attempts = result.get('attempts', NUM_ATTEMPTS)
            if result.get('result') == 'correct':
                result['game_status'] = 'win'
                base_score = NUM_WIN + (NUM_ATTEMPTS - attempts) * 100
            else:
                result['game_status'] = 'defeat'
                base_score = NUM_LOSS

            start_time = game_data.get('start_time', time.time())
            max_score = NUM_WIN + NUM_ATTEMPTS * 100
            min_time = 5      # segundos para máxima bonificación
            max_time = 120    # segundos para mínima bonificación

            final_score = calculate_score(base_score, start_time, max_score, min_time, max_time)
            save_score(request, 'adivinarnumero', final_score)
            result['final_score'] = final_score
            result['target'] = game.target  

        # Guarda el estado actualizado en la sesión
        request.session['adivina'] = game.get_state()
        request.session.modified = True

        return JsonResponse(result)
    except Exception as e:
        print("Error en play:", e)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def restartGame(request):
    request.session.pop('adivina', None)
    return JsonResponse({'status': 'success', 'message': 'Juego reiniciado'})

def giveup(request):
    adivina = request.session.get('adivina', {})
    attempts = adivina.get('attempts', NUM_ATTEMPTS)
    base_score = NUM_LOSS
    start_time = adivina.get('start_time', time.time())
    max_score = NUM_WIN + NUM_ATTEMPTS * 100
    min_time = 5
    max_time = 120

    final_score = calculate_score(base_score, start_time, max_score, min_time, max_time)
    save_score(request, 'adivinarnumero', final_score)
    request.session.pop('adivina', None)
    result = {
        'score': final_score,
        'message': 'Puntaje guardado',
        'target': adivina.get('target', None)  # <--- agrega esto
    }
    return JsonResponse(result)
