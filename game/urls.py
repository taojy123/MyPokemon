
from django.urls import path

from game.views import pokemon_init, new_game, game, join_game, card_action, game_attack, wild, wild_fight, match, \
    match_fight

urlpatterns = [
    path('pokemon/init/', pokemon_init),
    path('new/', new_game),
    path('game/<int:game_id>/', game),
    path('join/', join_game),
    path('card/<int:card_id>/action/', card_action),
    path('game/<int:game_id>/attack/', game_attack),
    path('wild/<int:wild_id>/', wild),
    path('wild/<int:wild_id>/fight/', wild_fight),
    path('match/<int:match_id>/', match),
    path('match/<int:match_id>/fight/', match_fight),
    # path('api/', api),
]
