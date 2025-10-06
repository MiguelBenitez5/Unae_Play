# app/piedrapapeltijera/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .piedrapapeltijera import PiedraPapelTijera
from globals.utils import is_session_active, save_score, calculate_score
import time
from globals.constants import RPS_ROUNDS, RPS_WIN, RPS_DRAW, RPS_LOSS

def renderPage(request):
    if not is_session_active(request):
        return redirect('login')
    if 'ppt' not in request.session:
        request.session['ppt'] = {
            'score': 0,
            'player_wins': 0,
            'machine_wins': 0,
            'draws': 0,
            'rounds_played': 0,
            'start_time': time.time(),  # Guarda el tiempo de inicio
        }
    return render(request, 'piedrapapeltijera/piedrapapeltijera.html')

def play(request, player_choice):
    if not is_session_active(request):
        return JsonResponse({'status': 'error', 'message': 'Sesión no iniciada'})

    request.session.setdefault('ppt', {
        'score': 0,
        'player_wins': 0,
        'machine_wins': 0,
        'draws': 0,
        'rounds_played': 0,
        'start_time': time.time(),
    })

    game_data = request.session['ppt']
    ppt_game = PiedraPapelTijera(game_data)
    new_game_data = ppt_game.play_round(player_choice)

    # Guardar solo el estado relevante en sesión
    request.session['ppt'] = ppt_game.get_state()
    request.session.modified = True

    # Calcular y guardar puntaje si terminó
    if new_game_data.get('status') == 'finished':
        base_score = ppt_game.score
        start_time = game_data.get('start_time', time.time())
        max_score = RPS_ROUNDS * RPS_WIN  # Puntaje máximo posible
        min_time = 7      # segundos para máxima bonificación (ajusta según dificultad)
        max_time = 90     # segundos para mínima bonificación

        final_score = calculate_score(base_score, start_time, max_score, min_time, max_time)
        save_score(request, 'piedrapapeltijera', final_score)
        new_game_data['final_score'] = final_score

    return JsonResponse(new_game_data)

def restartGame(request):
    request.session.pop('ppt', None)
    return JsonResponse({'status': 'success', 'message': 'Juego reiniciado'})

def giveup(request):
    ppt = request.session.get('ppt', {})
    base_score = ppt.get('score', 0)
    start_time = ppt.get('start_time', time.time())
    max_score = RPS_ROUNDS * RPS_WIN
    min_time = 5
    max_time = 90

    final_score = calculate_score(base_score, start_time, max_score, min_time, max_time)
    save_score(request, 'piedrapapeltijera', final_score)
    request.session.pop('ppt', None)
    return JsonResponse({'score': final_score, 'message': 'Puntaje guardado'})