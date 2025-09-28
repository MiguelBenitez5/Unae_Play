from django.http import JsonResponse
from .models import Dialogue
from django.db.models.functions import Random


def get_dialogue(request,category:str, game:str):
    dialogue = Dialogue.objects.filter(category__category_name=category, game__game_name=game).order_by(Random()).values().first()
    if dialogue:
        return JsonResponse(dialogue)
    return JsonResponse({'error':'No se encontraron datos en la base de datos'})


    


