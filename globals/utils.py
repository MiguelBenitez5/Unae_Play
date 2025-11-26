from django.shortcuts import render
from .models import Score, Game, GlobalRank
from accounts.models import CustomUser
from django.db.models import Max, Sum
import language_tool_python
import time
from .config import END_GAME, START_GAME, WINNER_MESSAGE, END_MESSAGE, START_MESSAGE, PREV_MESSAGE, WINNER_TITLE, TITLE

#funciones en comun que se utilizan en varias aplicaciones

def is_session_active(request):
    if not request.session.get('access'):
        return False
    return True

def render_homepage(request):
    data = {}
    if END_GAME:
        data['end'] = True
    
    is_in_top_3 = False

    if not is_session_active(request):
        data['logged'] = False
    else:
        data['logged'] = True
        user_id = request.session.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        data['winner'] = False
        is_in_top_3 = GlobalRank.objects.filter(user=user)[:3].exists()
        if is_in_top_3 and END_GAME:
            data['winner'] = True
    
    data['title'] = get_title(is_in_top_3)
    data['message'] = get_message(END_GAME, START_GAME, is_in_top_3)

    return render(request, 'index.html', data)

def get_message(is_end,is_start, is_winner):
    if is_end:
        if is_winner:
            return WINNER_MESSAGE
        return END_MESSAGE
    if is_start:
        return START_MESSAGE
    
    return PREV_MESSAGE

def get_title(is_winner):
    if END_GAME and is_winner:
        return WINNER_TITLE
    return TITLE


def save_score(request, game_name:str, score:int) -> None:
    #solo se guardan los puntajes cuando comience la competencia hasta llegar al final
    if not START_GAME or END_GAME:
        return
    user_id = request.session.get('user_id')
    user = CustomUser.objects.get(id=user_id)
    game = Game.objects.get(game_name = game_name)
    # Comprobar puntaje maximo para compararlo con el puntaje actual
    max_score = Score.objects.filter(game=game, user=user).aggregate(Max('score'))
    # Si el jugador obtiene un nuevo mejor puntaje, se recalcula su posicion en el ranking, si es su primer puntaje
    # se registra en el rankig global
    if max_score and (max_score['score__max'] or 0) < score:
        total = Score.objects.filter(user=user).values('game').annotate(best_scores=Max('score')).aggregate(total_score=Sum('best_scores'))
        # aqui utilizo un _ para indicar que no utilizare la variable que en este caso se trata de created que retorna True o False en caso de ser primer, registro o actualizacion
        global_rank, _ = GlobalRank.objects.update_or_create(user=user,defaults={'score': total['total_score'] or 0})
    score = Score(game = game, user = user, score = score)
    score.save()
    

def correct_word(userword):
    tool = language_tool_python.LanguageTool('es', remote_server='https://api.languagetool.org')
    matches = tool.check(userword)

    corrected = language_tool_python.utils.correct(userword, matches)

    return corrected


"""
Se calcula el pruntaje conforme al estandar de los minijuegos de la pagina\n
---------------------------------------------------------------------------
Params:
    score (int): La puntuacion del jugador al finalizar el juego\n
    start_time (int o float): El tiempo de inicio de la partida en milisegundos\n
    max_score (int): Puntaje maximo del juego\n
    min_time (int): Tiempo record en que tomaria ganar la partida al jugador en milisegundos\n
    max_time (int): Tiempo maximo tolerable para finalizar la partida y recibir bonificacion de puntaje en milisegundos\n
    time_weight[opcional] (float): Porcentaje de del valor del puntaje basado en el tiempo empleado\n  
"""
def calculate_score(score:int, start_time:int|float, max_score:int, min_time:int, max_time:int, time_weight:float=0.3)->int:
    score_norm = max(0,score/max_score)
    current_time = time.time()
    elapsed_time = current_time - start_time
    print(elapsed_time) 
    time_norm =  min(1, max(0, (max_time - elapsed_time)/(max_time-min_time)))
    score_percent = score_norm * ((1 + time_weight * time_norm) / (1 + time_weight))
    return int(score_percent * 1000)