from django.urls import path
from .views import render_page, play_wordle, reset_game

urlpatterns = [
    path('', render_page, name='wordle'),
    path('<str:userword>/',play_wordle ),
    path('action/restart/', reset_game),
]