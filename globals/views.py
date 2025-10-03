from django.http import JsonResponse
from .models import Dialogue, Game, Score, GlobalRank
from django.db.models.functions import Random
from accounts.models import CustomUser 


def get_dialogue(request,category:str, game:str):
    dialogue = Dialogue.objects.filter(category__category_name=category, game__game_name=game).order_by(Random()).values().first()
    if dialogue:
        return JsonResponse(dialogue)
    return JsonResponse({'error':'No se encontraron datos en la base de datos'})

def get_all_scores(request, game):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'status':'error','message':'No se pudo acceder a la sesion del usuario'})
    user = CustomUser.objects.get(id=user_id)
    db_game = Game.objects.get(game_name=game)
    # puntaje de la ultima partida del jugador
    score_object = Score.objects.filter(user=user).latest()
    if not score_object:
        return JsonResponse({'status':'error','message':'No se pudo acceder al ultimo juego del usuario porque no existe'})
    # ranking del juego
    game_ranking = Score.objects.filter(game=db_game)[:10].values('user__username', 'score')
    if not game_ranking:
        return JsonResponse({'status':'error','message':'No se pudo acceder al ranking del juego porque no hay registros'})
    # ranking global
    global_rank = GlobalRank.objects.all()[:10].values('user__username', 'score')
    if not global_rank:
        return JsonResponse({'status':'error','message':'No se pudo acceder al ranking global porque aun no hay registros'})
    response = {
        'player_score': score_object.score,
        'game_ranking': list(game_ranking),
        'global_ranking': list(global_rank),
        'username': user.username  
    }

    return JsonResponse(response)
    








    


