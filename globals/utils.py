from django.shortcuts import render
from .models import Score, Game
from accounts.models import CustomUser

#funciones en comun que se utilizan en varias aplicaciones

def is_session_active(request):
    if not request.session.get('access'):
        return False
    return True

def render_homepage(request):
    return render(request, 'base.html')


def save_score(request, game_name:str, score:int) -> None:
    user_id = request.session.get('user_id')
    user = CustomUser.objects.get(id=user_id)
    game = Game.objects.get(game_name = game_name)
    score = Score(game = game, user = user, score = score)
    score.save()
