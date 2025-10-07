from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.render_reg, name= 'register'),
    path('login/', views.render_login, name = 'login'),
    path('logout/', views.logout, name='logout')
]