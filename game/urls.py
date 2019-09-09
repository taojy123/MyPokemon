
from django.urls import path

from game import apis
from game.views import pokemon_init, new_game, game, join_game, card_action, game_attack, wild, wild_fight, match, \
    match_fight

urlpatterns = [
    path('pokemon/init/', pokemon_init),
    path('new/', new_game),
    path('join/', join_game),
    path('game/<int:game_id>/', game),
    path('game/<int:game_id>/attack/', game_attack),
    path('card/<int:card_id>/action/', card_action),
    path('wild/<int:wild_id>/', wild),
    path('wild/<int:wild_id>/fight/', wild_fight),
    path('match/<int:match_id>/', match),
    path('match/<int:match_id>/fight/', match_fight),
    
    path('api/new/', apis.new_game),
    path('api/join/', apis.join_game),
    path('api/game_status/', apis.game_status),
    path('api/attack_wild/', apis.attack_wild),
    path('api/attack_player/', apis.attack_player),
    path('api/wild_status/', apis.wild_status),
    path('api/wild_fight/', apis.wild_fight),
    path('api/match_status/', apis.match_status),
    path('api/match_fight/', apis.match_fight),
]
