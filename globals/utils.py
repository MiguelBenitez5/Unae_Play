from django.shortcuts import render
from .models import Score, Game
from accounts.models import CustomUser
import language_tool_python

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

def correct_word(userword):
    tool = language_tool_python.LanguageTool('es', remote_server='https://api.languagetool.org')
    matches = tool.check(userword)

    corrected = language_tool_python.utils.correct(userword, matches)

    return corrected

