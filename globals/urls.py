from django.urls import path
from . import views

urlpatterns = [
    path('', views.rennder_homepage, name='homepage'),
]