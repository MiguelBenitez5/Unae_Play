from django.urls import path
from . import utils, views

urlpatterns = [
    path('', utils.render_homepage, name='homepage'),
    path('getdialogue/<str:category>/<str:game>/', views.get_dialogue),
]