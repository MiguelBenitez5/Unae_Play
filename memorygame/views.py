from django.shortcuts import render, redirect
from globals.utils import is_session_active, save_score, calculate_score
import time
from django.http import JsonResponse
from .memorygame import MemoryGame

# Create your views here.

def render_page(request):
    if not is_session_active(request):
        return redirect('login')
    restart_game(request)
    return render(request, 'memorygame/memorygame.html',{'logged': True})

def play_game(request, position):
    try:
        row = int(position[0])
        col = int(position[2])
    except (ValueError, IndexError) as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Posición inválida: {str(e)}'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error inesperado: {str(e)}'
        })

    if not is_session_active(request):
        return JsonResponse({
            'status': 'error',
            'message': 'La sesión no está activa'
        })
    
    sessiondata = request.session.get('memorygame')
    if not sessiondata:
        return JsonResponse(
            {
                'status': 'error',
                'message': 'Error en la lectura de datos de sesion'
            }
        )
    
    memorygame = MemoryGame(sessiondata)

    response = memorygame.play_game(row, col)

    if not response:
        return JsonResponse({
            'status':'error',
            'message': 'El movimiento realizado es incorrecto'
        })
    
    response['status'] = 'success'

    #guardar datos en sesion
    if 'memorygame' not in request.session:
        return JsonResponse({
            'status': 'error', 
            'message': 'No existe la sesion memorygame'
        })
    
    request.session['memorygame'].update(response)
    request.session.modified = True

    # guardar puntaje
    if 'game_status' in response:
        match response['game_status']:
            case 'win':
                score = response['score']
                start_time = request.session['memorygame']['start_time']
                max_score = 1600
                min_time = 15
                max_time = 120
                final_score = calculate_score(score,start_time,max_score,min_time,max_time)
                save_score(request,'memorygame',final_score)

    response['position_1'] = request.session['memorygame']['position_1']
    response['board'] = None

    return JsonResponse(response)


def init_game(request):
    request.session.setdefault('memorygame',{
        'start_time': time.time(),
        'board': None,
        'user_choose_1': None,
        'user_choose_2': None,
        'position_1': None,
        'position_2': None,
        'pairs': 0,
        'score': 0,
        'tries': 0
    })

def give_up(request):
    session_data = request.session.get('memorygame')

    if not session_data:
        return JsonResponse({'status': 'error', 'message': 'No se encontraron datos en la sesion'})
    
    score = session_data.get('score', 0)
    start_time = session_data.get('start_time')
    max_score = 1600
    min_time = 15
    max_time = 120
        
    final_score = calculate_score(score, start_time, max_score, min_time, max_time)

    save_score(request, 'memorygame', final_score)
    restart_game(request)
    return JsonResponse({"score": score})
    
def restart_game(request):
    request.session.pop('memorygame', None)
    request.session.modified = True
    init_game(request)
    return JsonResponse({
        'status': 'success',
        'message': 'Partida reestablecida correctamente'
    })