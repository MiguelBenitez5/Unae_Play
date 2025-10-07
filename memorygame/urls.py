from django.urls import path
from .views import render_page, restart_game, play_game, give_up

urlpatterns = [
    path('', render_page, name='memorygame'),
    path('<str:position>/', play_game),
    path('action/restart/', restart_game),
    path('action/giveup/', give_up)
]