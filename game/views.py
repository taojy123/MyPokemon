import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from game.models import Game, Card, Wild, Battle
from game.pokemon_init import init


def pokemon_init(request):
    init()
    return HttpResponse('init ok')


@login_required
def new_game(request):
    name = request.POST.get('name')
    if not name:
        name = 'test'
    game, _ = Game.objects.get_or_create(name=name)
    game.init()
    player = game.add_player(request.user)
    player.turn = True
    player.save()
    return HttpResponseRedirect(f'/game/game/{game.id}/')


@login_required
def game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'game.html', locals())


@login_required
def add_player(request):
    game_id = request.POST.get('game_id')
    init_card_id = request.POST.get('init_card_id')
    is_ai = request.POST.get('is_ai')
    game = get_object_or_404(Game, id=game_id)
    if is_ai:
        game.add_player()
    else:
        init_card = Card.objects.filter(game=game, level=1, status=0, player=None, id=init_card_id).first()
        game.add_player(request.user, init_card)
    return HttpResponseRedirect(f'/game/game/{game.id}/')


@login_required
def card_action(request, card_id):
    action = request.POST.get('action')
    card = get_object_or_404(Card, id=card_id)
    game = card.game
    player = game.turn_player
    assert card.player.user == player.user == request.user, (card.id, request.user)
    if action == 'learn':
        skill = card.learn()
        messages.info(request, f'{card.pokemon} 学会技能 {skill}')
        game.next_turn()
    elif action == 'evo':
        evo_card = card.evo()
        if evo_card:
            messages.info(request, f'{card.pokemon} 进化为 {evo_card.pokemon}!')
            game.next_turn()
    elif action.startswith('add_'):
        kind = action[4:]
        if card.available_points > 0:
            card.extrapoint_set.create(kind=kind)
            messages.info(request, f'{card} 增加 1 点 {kind}')
            game.next_turn()
    elif action == 'rest':
        card.status = 2
        card.save()
        messages.info(request, f'{card} 休息')
    elif action == 'join':
        if player.cards1.count() < 6:
            card.status = 1
            card.save()
            messages.info(request, f'{card} 进入手牌')
            game.next_turn()
    return HttpResponseRedirect(f'/game/game/{game.id}/')


@login_required
def game_attack(request, game_id):
    name = request.POST.get('name')
    game = get_object_or_404(Game, id=game_id)
    assert game.turn_player.user == request.user, (game.id, request.user)
    player = game.player_set.get(user=request.user)
    if name == 'wild':
        ori_cards = game.card_set.filter(status=0, pokemon__pokemon__isnull=True)
        if not ori_cards.exists():
            game.join_cards()
            ori_cards = game.card_set.filter(status=0, pokemon__pokemon__isnull=True)
        card = random.choice(ori_cards)
        assert not card.player, card.id
        wild = player.wild_set.create(card=card)
        return HttpResponseRedirect(f'/game/wild/{wild.id}/')
    
    p = game.player_set.get(name=name)
    assert p != player, p.id
    match = player.player1_match_set.create(player2=p)
    return HttpResponseRedirect(f'/game/match/{match.id}/')


@login_required
def wild(request, wild_id):
    wild = get_object_or_404(Wild, id=wild_id)
    game = wild.game
    player = game.turn_player
    assert wild.player.user == request.user
    assert game.turn_player.user == request.user
    battle = wild.battles.first()
    if battle:
        for t in battle.texts:
            messages.info(request, t)
    for t in wild.texts:
        messages.info(request, t)
    return render(request, 'wild.html', locals())


@login_required
def fight(request, wild_id):
    wild = get_object_or_404(Wild, id=wild_id)
    game = wild.game
    player = game.turn_player
    assert wild.player.user == player.user == request.user
    assert not wild.events, wild.id
    card_id = request.POST.get('card_id')
    if card_id:
        card = get_object_or_404(Card, game=game, player=player, status=1, id=card_id)
        battle = Battle.objects.create(card1=card, card2=wild.card)
        battle.fight()
        wild.battles.add(battle)
        wild.winner = battle.winner
        wild.save()
        if wild.winner == 1:
            wild_card = wild.card
            wild.events += f'战胜 {wild_card}\n'
            
            total_exp = wild_card.attack + wild_card.defense + wild_card.hp
            remain_cards = player.card_set.filter(status=1).exclude(id=card.id)
            remain_count = remain_cards.count()
            if remain_count <= 0:
                card.gain_exp(total_exp)
                wild.events += f'{card.pokemon} 获得 {total_exp} 经验值\n'
            else:
                card.gain_exp(total_exp / 2)
                wild.events += f'{card.pokemon} 获得 {total_exp / 2} 经验值\n'
                for c in remain_cards:
                    c.gain_exp(total_exp / 2 / remain_count)
                    wild.events += f'{c.pokemon} 获得 {total_exp / 2 / remain_count} 经验值\n'
            
            if random.randint(1, 5) == 1:
                # 五分之一几率捕获精灵
                wild_card.player = player
                wild_card.status = 1
                wild_card.save()
                wild.events += f'捕获了 {wild_card.pokemon}!\n'
            
        else:
            wild.events += f'战斗失败，{card} 必须休息\n'
            card.status = 2
            card.save()
    else:
        wild.winner = -1
        wild.save()
        wild.events += f'逃跑了\n'
        
    wild.save()
    game.next_turn()
    
    return HttpResponseRedirect(f'/game/wild/{wild.id}/')


@login_required
def match(request, match_id):
    match = get_object_or_404(Wild, id=match_id)
    game = match.game
    player = game.turn_player
    assert wild.player.user == request.user
    assert game.turn_player.user == request.user
    battle = wild.battles.first()
    if battle:
        for t in battle.texts:
            messages.info(request, t)
    for t in wild.texts:
        messages.info(request, t)
    return render(request, 'match.html', locals())


