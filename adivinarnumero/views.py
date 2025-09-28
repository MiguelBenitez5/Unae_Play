# app/adivinarnumero/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .adivinarnumero import AdivinarNumero
from globals.utils import is_session_active, save_score

def renderPage(request):
    if not is_session_active(request):
        return redirect('login')
    return render(request, 'adivinarnumero/adivinarnumero.html')

def play(request, number):
    if not is_session_active(request):
        return JsonResponse({'status': 'error', 'message': 'Sesión no iniciada'})

    # Usamos setdefault para asegurar que la estructura base exista, pero 
    # OMITIMOS 'target' y 'start_time' para que AdivinarNumero.__init__ genere 
    # los valores aleatorios iniciales la primera vez.
    request.session.setdefault('adivina', {
        'attempts': 0,
        'score': 0,
    })

    game_data = request.session['adivina']
    game = AdivinarNumero(game_data)

    # 'number' ya viene como int gracias a la URL
    result = game.guess(number)
    
    # Si el juego ha terminado, incluimos el número secreto ('target') en la respuesta.
    if result['finished']:
        result['target'] = game.target
        save_score(request, 'adivinarnumero', game.score)

    request.session['adivina'] = game.get_state()
    request.session.modified = True

    return JsonResponse(result)

def restartGame(request):
    request.session.pop('adivina', None)
    return JsonResponse({'status': 'success', 'message': 'Juego reiniciado'})

def giveup(request):
    score = request.session.get('adivina', {}).get('score', 0)
    save_score(request, 'adivinarnumero', score)
    request.session.pop('adivina', None)
    return JsonResponse({'score': score, 'message': 'Puntaje guardado'})
