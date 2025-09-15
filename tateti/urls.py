from django.urls import path

from . import views

urlpatterns = [
    path('', views.renderPage),
    path('<str:position>/', views.playTateti),
    path('action/restart/', views.restartGame),
    path('action/nextlevel/', views.next_level),
    path('action/giveup/', views.giveup),
]