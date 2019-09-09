import random
from functools import wraps

from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.http.response import HttpResponseBase, JsonResponse
from django.shortcuts import render, get_object_or_404

from game.models import Game, Card, Wild, Battle, Match, Pokemon
from game.pokemon_init import init


def get_param(request, name, default=None):
    return request.GET.get(name, request.POST.get(name, default))


def pokemon_api(view_func):
    
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = get_param(request, 'token')
        game_id = get_param(request, 'game_id')
        match_id = get_param(request, 'match_id')
        wild_id = get_param(request, 'wild_id')
        
        if not token:
            return HttpResponseForbidden('miss token (username:password)')
        if token.count(':') != 1:
            return HttpResponseForbidden('invalid token')
        username, password = token.split(':')
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
        if not user.check_password(password):
            return HttpResponseForbidden('invalid password')
        if not user.is_active:
            return HttpResponseForbidden('unavailable user')

        request.user = user
        request.game = None
        request.match = None
        request.wild = None
        request.player = None

        if match_id:
            match = get_object_or_404(Match, id=match_id)
            request.match = match
            request.game = match.game

        if wild_id:
            wild = get_object_or_404(Wild, id=wild_id)
            request.wild = wild
            request.game = wild.game
            
        if game_id:
            game = get_object_or_404(Game, id=game_id)
            request.game = game

        if request.game:
            player = request.game.player_set.filter(user=user).first()
            request.player = player
            
        result = view_func(request, *args, **kwargs)
        if not result:
            result = HttpResponse()
        if not isinstance(result, HttpResponseBase):
            result = JsonResponse(result, safe=False)
        return result
    
    return _wrapped_view


@pokemon_api
def new_game(request):
    name = get_param(request, 'name')
    pokemon_id = get_param(request, 'pokemon_id')
    if pokemon_id:
        pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    else:
        pokemon = None
    game = Game.new(request.user, name, pokemon)
    return game.to_dict()


@pokemon_api
def join_game(request):
    is_ai = get_param(request, 'is_ai')
    game = request.game
    if is_ai:
        game.join_game()
    else:
        game.join_game(request.user)
    return game.to_dict()


@pokemon_api
def game_status(request):
    game = request.game
    return game.to_dict()


@pokemon_api
def attack_wild(request):
    game = request.game
    assert game.turn_player.user == request.user
    wild = game.attack_wild()
    return wild.to_dict()


@pokemon_api
def attack_player(request):
    name = get_param(request, 'name')
    game = request.game
    assert game.turn_player.user == request.user
    p = game.player_set.get(name=name)
    match = game.attack_player(p)
    return match.to_dict()


@pokemon_api
def wild_status(request):
    wild = request.wild
    return wild.to_dict()


@pokemon_api
def wild_fight(request):
    wild = request.wild
    game = wild.game
    player = game.turn_player
    assert wild.player == request.player == player
    assert not wild.events, wild.id

    card_id = get_param(request, 'card_id')
    if card_id:
        card = get_object_or_404(Card, game=game, player=player, status=1, id=card_id)
    else:
        card = None

    wild.fight(card)

    return wild.to_dict()


@pokemon_api
def match_status(request):
    match = request.match
    return match.to_dict()


@pokemon_api
def match_fight(request):

    card_id = get_param(request, 'card_id')

    match = request.match
    game = match.game
    player = request.player

    card = get_object_or_404(Card, game=game, player=player, status=1, id=card_id)
    match.fight(card)

    return match.to_dict()


