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
    assert card.player.user == request.user, (card.id, request.user)
    assert game.turn_player.user == request.user, (game.id, request.user)
    if action == 'learn':
        skill = card.learn()
        messages.info(request, f'{card.pokemon} 学会技能 {skill}')
        game.next_turn()
    elif action == 'evo':
        new_card = card.evo()
        if new_card:
            messages.info(request, f'{card.pokemon} 进化为 {new_card.pokemon}!')
            game.next_turn()
    elif action == 'out':
        if card.status == 2:
            card.status = 1
            card.save()
            messages.info(request, f'{card} 进入手牌')
            game.next_turn()
    return HttpResponseRedirect(f'/game/game/{game.id}/')


@login_required
def game_action(request, game_id):
    action = request.POST.get('action')
    game = get_object_or_404(Game, id=game_id)
    assert game.turn_player.user == request.user, (game.id, request.user)
    player = game.player_set.get(user=request.user)
    if action == 'wild':
        ori_cards = game.card_set.filter(status=0, pokemon__pokemon__isnull=True)
        if not ori_cards.exists():
            messages.info(request, f'牌堆已空，无法打野')
            return HttpResponseRedirect(f'/game/game/{game.id}/')
        card = random.choice(ori_cards)
        assert not card.player, card.id
        wild = player.wild_set.create(card=card)
        return HttpResponseRedirect(f'/game/wild/{wild.id}/')
        
    elif action == 'match':
        pass
        
    return HttpResponseRedirect(f'/game/game/{game.id}/')


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
    return render(request, 'wild.html', locals())


@login_required
def fight(request, wild_id):
    wild = get_object_or_404(Wild, id=wild_id)
    game = wild.game
    assert wild.player.user == request.user
    assert game.turn_player.user == request.user
    player = game.turn_player
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
            messages.info(request, f'战胜 {wild_card}')
            
            total_exp = wild_card.attack + wild_card.defense + wild_card.hp
            remain_cards = player.card_set.filter(status=1).exclude(id=card.id)
            remain_count = remain_cards.count()
            if remain_count <= 0:
                card.gain_exp(total_exp)
                messages.info(request, f'{card.pokemon} 获得 {total_exp} 经验值')
            else:
                card.gain_exp(total_exp / 2)
                messages.info(request, f'{card.pokemon} 获得 {total_exp / 2} 经验值')
                for c in remain_cards:
                    c.gain_exp(total_exp / 2 / remain_count)
                    messages.info(request, f'{c.pokemon} 获得 {total_exp / 2 / remain_count} 经验值')
            
            if random.randint(1, 5) == 1:
                # 五分之一几率捕获精灵
                wild_card.player = player
                wild_card.status = 1
                wild_card.save()
                messages.info(request, f'捕获了 {wild_card.pokemon}!')
            
        else:
            messages.info(request, f'战斗失败')
            card.status = 2
            card.save()
    else:
        wild.winner = -1
        wild.save()
        messages.info(request, f'逃跑了')
        
    game.next_turn()
    
    return HttpResponseRedirect(f'/game/wild/{wild.id}/')


