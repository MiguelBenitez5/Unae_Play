from django.urls import path
from . import utils

urlpatterns = [
    path('', utils.render_homepage, name='homepage'),
]