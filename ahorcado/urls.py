from django.urls import path
from .views import render_page, play_game, restart_game, get_data

urlpatterns = [
    path('', render_page, name='ahorcado'),
    path('<str:userchar>/', play_game),
    path('action/restart', restart_game),
    path('action/getdata', get_data),
]