# app/adivinarnumero/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.renderPage, name='adivinarnumero'),
    path('play/<int:number>/', views.play, name='adivinar_play'),
    path('action/restart/', views.restartGame, name='adivinar_restart'),
    path('action/giveup/', views.giveup, name='adivinar_giveup'),
]
