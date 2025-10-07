from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_page, name='buscaminas_game'),
    path('start/', views.start_game, name='start_game'),
    path('reveal/<int:row>/<int:col>/', views.reveal_cell, name='reveal_cell'),
]
