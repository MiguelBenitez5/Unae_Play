from django.shortcuts import render, redirect
from globals.utils import is_session_active
import time
from django.http import JsonResponse
from .memorygame import MemoryGame

# Create your views here.

def render_page(request):
    if not is_session_active(request):
        return redirect('login')
    restart_game(request)
    init_game(request)
    return render(request, 'memorygame/memorygame.html')

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
    
    return JsonResponse(response)


def init_game(request):
    request.session.setdefault('memorygame',{
        'start_time': time.time(),
        'board': None,
        'user_choose_1': None,
        'user_choose_2': None,
        'pairs': 0,
        'score': 0
    })

def restart_game(request):
    request.session.pop('memorygame', None)
    request.session.modified = True