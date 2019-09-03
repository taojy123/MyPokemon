
from django.urls import path

from game.views import pokemon_init, new_game, game, add_player, card_action, game_action, wild, fight

urlpatterns = [
    path('pokemon/init/', pokemon_init),
    path('new_game/', new_game),
    path('game/<int:game_id>/', game),
    path('add_player/', add_player),
    path('card/<int:card_id>/action/', card_action),
    path('game/<int:game_id>/action/', game_action),
    path('wild/<int:wild_id>/', wild),
    path('wild/<int:wild_id>/fight/', fight),
]
