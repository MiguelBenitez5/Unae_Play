from django.urls import path
from . import utils, views

urlpatterns = [
    path('', utils.render_homepage, name='homepage'),
    path('getdialogue/<str:category>/<str:game>/', views.get_dialogue),
    path('getscores/<str:game>', views.get_all_scores),
    path('globalrank/', views.get_global_ranking),
    path('campaign/follow', views.click_campaign),
]