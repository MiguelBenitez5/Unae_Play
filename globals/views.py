from django.shortcuts import render
from django.http import JsonResponse
from .models import Dialogue, Game, Score, GlobalRank, BugReport
from django.db.models.functions import Random
from accounts.models import CustomUser
from .utils import is_session_active
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile 

def report_bug(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id', None)
        if not user_id:
            username = 'Anonimo'
        else:
            user = CustomUser.objects.filter(id=user_id).first()
            if not user:
                username = 'Anonimo'
            else:
                username = user.username
        
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        if 'image' in request.FILES:
            image = request.FILES.get('image')
            report = BugReport(username=username, subject=subject, description=description, image=image)
        else:
            report = BugReport(username=username,subject=subject, description=description)
        
        report.save()

    is_logged = is_session_active(request)

    return render(request, 'report.html', {'logged': is_logged})
        

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
    
"""
Se obtienen los 10 primeros registros del ranking global ordenados de mayor a menor
"""
def get_global_ranking(request):
    context = {'logged': True, 'clicked': False}
    if not is_session_active(request):
        context['logged'] = False
        context['clicked'] = True #cuando no esta logueado no se mostrara la campaña
    user_id = request.session.get('user_id')   

    user = CustomUser.objects.get(id=user_id)
    context['clicked'] = user.clicked_campaign 
    
    global_rank = GlobalRank.objects.all()[:10].values('user__username', 'score')
    context['global_rank'] = global_rank
    return render(request, 'global_rank.html', context)

"""
Otorga 100 puntos a aquellos usuarios que sigan al perfil de 
instagram del sponsor
"""
def click_campaign(request):
    if not is_session_active(request):
        return JsonResponse({'status':'error'})
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'status':'error'})
    user = CustomUser.objects.get(id=user_id)
    if not user.clicked_campaign:
        user_score = GlobalRank.objects.filter(user=user).values('score').first() or 0
        total_score = user_score['score'] + 100
        _,_ = GlobalRank.objects.update_or_create(user=user, defaults={'score': total_score })
        user.clicked_campaign = True
        user.save()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status':'error'})


"""
Muestra la pagina de preguntas frecuentes
"""
def render_faq(request):
    if not is_session_active(request):
        return render(request, 'faq.html', {'logged': False})
    return render(request, 'faq.html', {'logged': True})
    

