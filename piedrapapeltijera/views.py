# # app/piedrapapeltijera/views.py
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from .piedrapapeltijera import PiedraPapelTijera
# from globals.utils import is_session_active, save_score

# def renderPage(request):
#     if not is_session_active(request):
#         return redirect('login')
#     return render(request, 'piedrapapeltijera/piedrapapeltijera.html')

# def play(request, player_choice):
#     if not is_session_active(request):
#         return JsonResponse({'status': 'error', 'message': 'Sesión no iniciada'})

#     request.session.setdefault('ppt', {
#         'score': 0,
#         'player_wins': 0,
#         'machine_wins': 0,
#         'draws': 0,
#     })

#     game_data = request.session['ppt']
#     ppt_game = PiedraPapelTijera(game_data)
    
#     new_game_data = ppt_game.play_round(player_choice)
    
#     request.session['ppt'] = new_game_data
#     request.session.modified = True
    
#     return JsonResponse(new_game_data)

# def restartGame(request):
#     request.session.pop('ppt', None)
#     return JsonResponse({'status': 'success', 'message': 'Juego reiniciado'})

# def giveup(request):
#     score = request.session.get('ppt', {}).get('score', 0)
#     save_score(request, 'piedrapapeltijera', score)
#     request.session.pop('ppt', None)
#     return JsonResponse({'score': score, 'message': 'Puntaje guardado'})

# app/piedrapapeltijera/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .piedrapapeltijera import PiedraPapelTijera
from globals.utils import is_session_active, save_score

def renderPage(request):
    if not is_session_active(request):
        return redirect('login')
    return render(request, 'piedrapapeltijera/piedrapapeltijera.html')

# def play(request, player_choice):
    # if not is_session_active(request):
    #     return JsonResponse({'status': 'error', 'message': 'Sesión no iniciada'})

    # request.session.setdefault('ppt', {
    #     'score': 0,
    #     'player_wins': 0,
    #     'machine_wins': 0,
    #     'draws': 0,
    # })

    # game_data = request.session['ppt']
    # ppt_game = PiedraPapelTijera(game_data)
    
    # new_game_data = ppt_game.play_round(player_choice)
    
    # request.session['ppt'] = new_game_data
    # request.session.modified = True
    
    # return JsonResponse(new_game_data)
# def play(request, player_choice):
#     if not is_session_active(request):
#         return JsonResponse({'status': 'error', 'message': 'Sesión no iniciada'})

#     request.session.setdefault('ppt', {
#         'score': 0,
#         'player_wins': 0,
#         'machine_wins': 0,
#         'draws': 0,
#         'rounds_played': 0,
#     })

#     game_data = request.session['ppt']
#     ppt_game = PiedraPapelTijera(game_data)

#     new_game_data = ppt_game.play_round(player_choice)

#     # Guardar solo el estado relevante
#     request.session['ppt'] = ppt_game.get_state()
#     request.session.modified = True

#     return JsonResponse(new_game_data)
# app/piedrapapeltijera/views.py

def play(request, player_choice):
    if not is_session_active(request):
        return JsonResponse({'status': 'error', 'message': 'Sesión no iniciada'})

    request.session.setdefault('ppt', {
        'score': 0,
        'player_wins': 0,
        'machine_wins': 0,
        'draws': 0,
        'rounds_played': 0,
    })

    game_data = request.session['ppt']
    ppt_game = PiedraPapelTijera(game_data)

    new_game_data = ppt_game.play_round(player_choice)

    # Guardar solo el estado relevante en sesión
    request.session['ppt'] = ppt_game.get_state()
    request.session.modified = True

    # 👇 Guardar puntaje automáticamente si terminó
    if new_game_data.get('status') == 'finished':
        save_score(request, 'piedrapapeltijera', ppt_game.score)

    return JsonResponse(new_game_data)

def restartGame(request):
    request.session.pop('ppt', None)
    return JsonResponse({'status': 'success', 'message': 'Juego reiniciado'})

def giveup(request):
    score = request.session.get('ppt', {}).get('score', 0)
    save_score(request, 'piedrapapeltijera', score)
    request.session.pop('ppt', None)
    return JsonResponse({'score': score, 'message': 'Puntaje guardado'})