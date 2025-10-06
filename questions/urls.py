from django.urls import path
from .views import render_page, request_question, answer_question, give_up

urlpatterns = [
    path('', render_page, name='questions'),
    path('answer', answer_question),
    path('action/request', request_question),
    path('action/giveup/', give_up),
]