# app/piedrapapeltijera/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.renderPage, name='piedrapapeltijera'),
    path('play/<str:player_choice>/', views.play),
    path('action/restart/', views.restartGame),
    path('action/giveup/', views.giveup),
]