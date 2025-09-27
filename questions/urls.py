from django.urls import path
from .views import render_page, request_question, answer_question

urlpatterns = [
    path('', render_page, name='questions'),
    path('<str:answer>/', answer_question),
    path('action/request', request_question)
]