from django.urls import path

from . import views

urlpatterns = [
    path('', views.renderPage),
    path('<str:position>', views.playTateti),
    path('restart', views.restartGame)
]