from django.shortcuts import render, redirect
from django.http import JsonResponse
from .tateti import Tateti
import time
from globals.utils import is_session_active, save_score

# Create your views here.
def restartGame(request):
    request.session.pop('tateti', None)
    return JsonResponse({'status': 'success', 'message': 'La sesion fue eliminada correctamente'})

def renderPage(request):
    #comprobar que el usuario esta loguedado para acceder al juego
    if not is_session_active(request):
        return redirect('login')
    #aqui se pasa la logica que se quiera renderizar en la pagina 
    return render(request, 'tateti/tateti.html')

def next_level(request):
    level = request.session.get('tateti',{}).get('level', 'easy')
    board = [[" " for _ in range(3)] for _ in range(3)]
    match level:
        case 'easy':
            level = 'medium'
        case 'medium':
            level = 'hard'

    response = {}
    machine_moves = 0

    if 'hard_machine_move' in request.session['tateti']:
        machine_moves = 1
        board = request.session['tateti']['hard_machine_move']['board']
        response['hard_machine_move'] = {
            'board': board
        }
    restart_values = {
            'level': level, 
            'board': board,
            'player_moves': 0,
            'machine_moves': machine_moves,
            'player_draws': 0,
        } 
    request.session['tateti'].update(restart_values)
    request.session.modified = True
    dialog = request.session.get('dialog', None)
    response['level'] = level 
    response['dialog'] = dialog


    return JsonResponse(response)

def giveup(request):
    request.session.setdefault('tateti',{ 'score': 0})
    score = request.session['tateti']['score']
    save_score(request, 'tateti', score)
    #en el futuro tambien se retornara el resultado de los rankings
    restartGame(request)
    return JsonResponse({'score': score})

"""
Realiza la jugada, recibiendo la peticion del cliente y envia los resultados a traves de on JSON\n
Estados retornados:
    -status : error (cuando la jugada es incorrecta)
    -status : success (cuando la jugada se realizo correctamente)
Estado de la partida retornados:
    -game_status : 0 (la partida continua, aun no esta definodo el ganador o empate)
    -game_status : win (el jugador gana la partida, es decir logra vencer a la maquina en todas sus dificultades)
"""
def playTateti(request,position):

    #comprobando la sesion del usuario
    if not is_session_active(request):
        return JsonResponse({'status':'error',
                             'message':'No se puede realizar la jugada porque la sesion no esta iniciada'})
    
    row = int(position[0])
    column = int(position[2])
    print(row)
    print(column)

    ##comprobar posiciones correctas
    if row > 2 or row < 0 or column > 2 or column < 0:
        return JsonResponse({
                'status':'error',
                'message':'Posicion incorrecta, fuera de rango',
            })

    #asignar valores por defecto para la partida
    board = [[" " for _ in range(3)] for _ in range(3)]
    request.session.setdefault('tateti',{
        'start_time':time.time(),
        'score': 0,
        'board': board,
        'level':'easy',
        'player_moves': 0,
        'machine_moves': 0,
        'player_draws': 0,
    })

    #recuperar los valores de la sesion (si no existen se utilizan los valores por defecto)
    session_data = request.session.get('tateti')

    #se crea el objeto tateti con los datos de sesion
    tateti = Tateti(session_data)

    game_data = tateti.play_game(row, column)

    #probando
    board = request.session.get('tateti', {}).get('board', 'Prueba1')
    level = request.session.get('tateti', {}).get('level', 'Prueba2')

    #comprobar si la jugada es correcta
    if not game_data:
        return JsonResponse(
            {
                'status':'error',
                'message': 'Jugada incorrecta',
                'board': board,
                'level': level,
            }
        )

    #guardar resultados en la base de datos al finalizar partida
    match game_data['game_status']:
        case 'win':
            if game_data['level'] == 'hard':
                save_score(request,'tateti', game_data['score'])
        case 'defeat': 
            save_score(request, 'tateti', game_data['score'])
    
    #se guardan los datos en sesion
    request.session['tateti'] = game_data
    #se retorna la respuesta al cliente
    return JsonResponse(game_data)
   

