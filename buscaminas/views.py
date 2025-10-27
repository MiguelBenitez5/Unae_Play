from django.http import JsonResponse
from django.shortcuts import render, redirect
from globals.utils import save_score, is_session_active, calculate_score
from .game_logic import Minesweeper
from accounts.models import CustomUser
import logging

# Configurar logging simple
logger = logging.getLogger(__name__)

# Diccionario global de partidas por sesión
games = {}

# ------------------------------
# Funciones de utilidad
# ------------------------------
def ensure_user_session(request):
    """Asegura que haya sesión y usuario válido"""
    if not request.session.session_key:
        request.session.save()
    user_id = request.session.get('user_id')
    if not user_id:
        user = CustomUser.objects.first()
        if not user:
            raise Exception("No users in DB")
        request.session['user_id'] = user.id
    return request.session['user_id']

def get_user_game(request):
    """Obtiene la partida asociada a la sesión"""
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key
    return games.get(session_key)

def get_visible_board(game):
    """Devuelve solo los valores de las celdas reveladas"""
    return [
        [game.board[r][c] if game.revealed[r][c] else None for c in range(game.cols)]
        for r in range(game.rows)
    ]

def reveal_all(game):
    """Devuelve todas las celdas (para game over)"""
    return [[game.board[r][c] for c in range(game.cols)] for r in range(game.rows)]

# ------------------------------
# Vistas
# ------------------------------
def game_page(request):
    """Renderiza la página principal del juego"""
    if not is_session_active(request):
        return redirect('login')
    try:
        ensure_user_session(request)
        return render(request, 'buscaminas.html', {'logged': True})
    except Exception as e:
        logger.error(f"Error en game_page: {e}")
        return JsonResponse({"error": str(e)}, status=500)

def start_game(request):
    """Inicia una nueva partida"""
    try:
        ensure_user_session(request)
        game = Minesweeper(rows=8, cols=8, mines=10)
        games[request.session.session_key] = game
        return JsonResponse({"status": "started"})
    except Exception as e:
        logger.error(f"Error al iniciar juego: {e}")
        return JsonResponse({"error": str(e)}, status=500)

def restart_game(request):
    """Reinicia la partida actual y devuelve el nuevo tablero vacío"""
    try:
        ensure_user_session(request)
        session_key = request.session.session_key

        # Si no hay partida activa, simplemente crea una nueva
        if session_key not in games:
            games[session_key] = Minesweeper(rows=8, cols=8, mines=10)
        else:
            # Reinicia la partida existente
            games[session_key].reset()

        return JsonResponse({
            "status": "restarted",
            "board": [[None for _ in range(games[session_key].cols)] for _ in range(games[session_key].rows)]
        })
    except Exception as e:
        logger.error(f"Error al reiniciar juego: {e}")
        return JsonResponse({"error": str(e)}, status=500)

def reveal_cell(request, row, col):
    """Revela una celda del tablero"""
    try:
        ensure_user_session(request)
        game = get_user_game(request)
        if not game:
            return JsonResponse({"error": "No game in progress"}, status=400)

        # Validar coordenadas
        if row < 0 or row >= game.rows or col < 0 or col >= game.cols:
            return JsonResponse({"error": "Invalid cell"}, status=400)

        # Si es mina
        if game.is_mine(row, col):
            score = sum(sum(10 for c in row if c) for row in game.revealed)
            start_time = game.start_time
            max_points = 540
            min_time = 20
            max_time = 180
            final_score = calculate_score(score, start_time, max_points, min_time, max_time)
            try:
                save_score(request, "buscaminas", final_score)
            except Exception as e:
                logger.warning(f"Error al guardar score: {e}")
            return JsonResponse({"game_status": "defeat", "board": reveal_all(game)})

        # Revelar celda seleccionada
        game.reveal(row, col)

        # Si se completó el juego
        if game.is_finished():
            score = sum(sum(10 for c in row if c) for row in game.revealed)
            start_time = game.start_time
            max_points = 540
            min_time = 20
            max_time = 180
            final_score = calculate_score(score, start_time, max_points, min_time, max_time)
            try:
                save_score(request, "buscaminas", final_score)
            except Exception as e:
                logger.warning(f"Error al guardar score: {e}")
            return JsonResponse({"game_status": "win", "score": score, "board": reveal_all(game)})

        # Tablero visible hasta ahora
        return JsonResponse({"board": get_visible_board(game)})

    except Exception as e:
        logger.error(f"Error en reveal_cell: {e}")
        return JsonResponse({"error": str(e)}, status=500)

# TODO: Mejorar errores y verificacion por session activa u inactiva

def error_handler(request):
    return JsonResponse({"error": "An error occurred", "status": 500, "type": "TypeError"}, status=500)

def is_session_active(request):
    if not request.session.get('access'):
        return 0
    else:
        return 1
