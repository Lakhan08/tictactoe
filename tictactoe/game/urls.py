# game/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_game/', views.new_game, name='new_game'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('game/<int:game_id>/make_move/', views.make_move, name='make_move'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
