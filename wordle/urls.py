from django.urls import path
from .views import render_page, play_wordle, reset_game, get_initial_data

urlpatterns = [
    path('', render_page, name='wordle'),
    path('<str:userword>/',play_wordle ),
    path('action/restart/', reset_game),
    path('action/getdata/', get_initial_data),
]