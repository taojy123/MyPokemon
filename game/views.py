import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from game.models import Game, Card, Wild, Battle, Match
from game.pokemon_init import init


def pokemon_init(request):
    init()
    return HttpResponse('init ok')


@login_required
def new_game(request):
    name = request.POST.get('name')
    game = Game.new(request.user, None, name)
    return HttpResponseRedirect(f'/game/game/{game.id}/')


@login_required
def game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'game.html', locals())


@login_required
def join_game(request):
    game_id = request.POST.get('game_id')
    is_ai = request.POST.get('is_ai')
    game = get_object_or_404(Game, id=game_id)
    if is_ai:
        game.join_game()
    else:
        game.join_game(request.user)
    return HttpResponseRedirect(f'/game/game/{game.id}/')


@login_required
def card_action(request, card_id):
    action = request.POST.get('action')
    card = get_object_or_404(Card, id=card_id)
    assert card.player.user == request.user
    text = card.action(action)
    messages.info(request, text)
    return HttpResponseRedirect(f'/game/game/{game.id}/')


@login_required
def game_attack(request, game_id):
    name = request.POST.get('name')
    game = get_object_or_404(Game, id=game_id)
    assert game.turn_player.user == request.user

    if name == 'wild':
        wild = game.attack_wild()
        return HttpResponseRedirect(f'/game/wild/{wild.id}/')
    
    p = game.player_set.get(name=name)
    match = game.attack_player(p)
    return HttpResponseRedirect(f'/game/match/{match.id}/')


@login_required
def wild(request, wild_id):
    wild = get_object_or_404(Wild, id=wild_id)
    game = wild.game
    assert wild.player.user == request.user
    battle = wild.battles.first()
    if battle:
        for t in battle.texts:
            messages.info(request, t)
    for t in wild.texts:
        messages.info(request, t)
    return render(request, 'wild.html', locals())


@login_required
def wild_fight(request, wild_id):
    wild = get_object_or_404(Wild, id=wild_id)
    game = wild.game
    player = game.turn_player
    assert wild.player.user == player.user == request.user
    assert not wild.events, wild.id

    card_id = request.POST.get('card_id')
    if card_id:
        card = get_object_or_404(Card, game=game, player=player, status=1, id=card_id)
    else:
        card = None

    wild.fight(card)
    
    return HttpResponseRedirect(f'/game/wild/{wild.id}/')


@login_required
def match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    game = match.game
    player = request.user.player_set.get(game=game)
    assert player in [match.player1, match.player2]
    battles = match.battle_list
    if match.step_code in [1, 2] and not match.winner:
        match.winner = match.step_code
        match.events += f'{match.winner_player} 获得最终胜利!'
        match.save()
        game.next_turn()
    return render(request, 'match.html', locals())


@login_required
def match_fight(request, match_id):

    card_id = request.POST.get('card_id')

    card = get_object_or_404(Card, id=card_id)
    match = get_object_or_404(Match, id=match_id)

    assert card.player.user == request.user

    match.fight(card)

    return HttpResponseRedirect(f'/game/match/{match.id}/')


