import random

from django.contrib.auth.models import User
from django.db import models

from game.systems import SYSTEM_MAP


X_LEVEL_UP = 10


class Skill(models.Model):

    name = models.CharField(max_length=50, blank=True)
    system = models.CharField(max_length=10, blank=True)
    power = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.name}[{self.system}{self.power}]'
    
    def to_dict(self):
        return {
            'id': self.id,
            'str': str(self),
            'name': self.name,
            'system': self.system,
            'power': self.power,
        }


class Pokemon(models.Model):

    name = models.CharField(max_length=50, blank=True)
    no = models.IntegerField(default=0)
    system = models.CharField(max_length=20, blank=True)
    default_skill = models.ForeignKey(Skill, null=True, blank=True, on_delete=models.CASCADE)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    evo_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='pokemon', null=True, blank=True)

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'id': self.id,
            'str': str(self),
            'name': self.name,
            'no': self.no,
            'system': self.system,
            'default_skill': self.default_skill.to_dict() if self.default_skill else None,
            'attack': self.attack,
            'defense': self.defense,
            'hp': self.hp,
            'level': self.level,
            'evo_to': self.evo_to.to_dict() if self.evo_to else None,
            'pic': self.pic if self.pic else '',
        }


class Game(models.Model):
    name = models.CharField(max_length=50, blank=True)
    round = models.IntegerField(default=1)
    block = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    @classmethod
    def new(cls, user, name='', init_pokemon=None):
        if not name:
            name = 'test' + str(random.randint(100, 999))
        game = Game.objects.filter(name=name).first()
        if game:
            return game
        game = Game.objects.create(name=name)
        game.init()
        player = game.join_game(user, init_pokemon)
        player.turn = True
        player.save()
        return game
    
    @property
    def owner(self):
        return self.player_set.order_by('id').first()
    
    @property
    def players(self):
        return self.player_set.order_by('id')
    
    @property
    def turn_player(self):
        assert self.player_set.filter(turn=True).count() == 1, self.id
        return self.player_set.get(turn=True)
    
    @property
    def welcome(self):
        return f'欢迎来到 {self.owner} 创建的宠物小精灵世界!'
    
    @property
    def focus(self):
        wild = Wild.objects.filter(player__game=self, winner=0).order_by('-id').first()
        if wild:
            return wild
        match = Match.objects.filter(player1__game=self, winner=0).order_by('-id').first()
        if match:
            return match
        assert not self.block
        return self
    
    @property
    def focus_dict(self):
        focus = self.focus
        if isinstance(focus, Wild):
            category = 'wild'
        elif isinstance(focus, Match):
            category = 'match'
        else:
            category = 'game'
        return {
            'category': category,
            'id': focus.id
        }

    @property
    def step(self):
        focus = self.focus
        if isinstance(focus, Game):
            return 0, f'等待 {focus.turn_player} 操作'
        elif isinstance(focus, Match):
            return 1, f'{focus.player1} 与 {focus.player2} 正在对战'
        elif isinstance(focus, Wild):
            return 1, f'{focus.player} 野外遭遇 {focus.card}'
        assert False

    @property
    def step_code(self):
        return self.step[0]

    @property
    def step_display(self):
        return self.step[1]
    
    @property
    def selectable_cards(self):
        return Card.objects.filter(game=self, level=1, status=0, player=None)

    def init(self):
        assert not self.card_set.exists()
        assert not self.player_set.exists()
        self.join_cards()
            
    def join_cards(self):
        for p in Pokemon.objects.all():
            self.card_set.create(pokemon=p, level=p.level)

    def join_game(self, user=None, init_pokemon=None):
        if user:
            if self.player_set.filter(user=user).exists():
                return self.player_set.filter(user=user).first()
            player = self.player_set.create(user=user, name=user.username)
        else:
            name = f'AI{random.randint(100, 999)}'
            player = self.player_set.create(is_ai=True, name=name)

        selectable_cards = self.selectable_cards
        if init_pokemon:
            init_card = selectable_cards.filter(pokemon=init_pokemon).first()
        else:
            init_card = random.choice(selectable_cards)

        assert init_card
        init_card.player = player
        init_card.status = 1
        init_card.save()
        return player

    def attack_player(self, target_player):
        assert not self.block
        player = self.turn_player
        assert player != target_player
        match = player.player1_match_set.create(player2=target_player)
        self.block = True
        self.save()
        return match

    def attack_wild(self):
        assert not self.block
        player = self.turn_player
        # 牌堆里没有进化过的原始精灵
        ori_cards = self.card_set.filter(status=0, pokemon__pokemon__isnull=True)
        if not ori_cards.exists():
            self.join_cards()
            ori_cards = self.card_set.filter(status=0, pokemon__pokemon__isnull=True)
        wild_card = random.choice(ori_cards)
        assert not wild_card.player
        wild = player.wild_set.create(card=wild_card)
        self.block = True
        self.save()
        return wild

    def next_turn(self):
        self.block = False
        self.save()
        player = self.players.filter(id__gt=self.turn_player.id).first()
        if not player:
            player = self.players.first()
            self.round += 1
            self.save()
        self.players.update(turn=False)
        player.turn = True
        player.save()
        return player
    
    def to_dict(self):
        return {
            'id': self.id,
            'str': str(self),
            'name': self.name,
            'round': self.round,
            'block': self.block,
            'owner': self.owner.to_dict(),
            'turn_player': self.turn_player.to_dict(),
            'players': [p.to_dict() for p in self.players],
            'welcome': self.welcome,
            'focus': self.focus_dict,
            'step': self.step,
            'step_code': self.step_code,
            'step_display': self.step_display,
            'selectable_cards': [c.to_dict() for c in self.selectable_cards],
        }


class Player(models.Model):
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    is_ai = models.BooleanField(default=False)
    turn = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    @property
    def cards(self):
        return self.card_set.order_by('status')
    
    @property
    def cards1(self):
        return self.card_set.filter(status=1)
    
    @property
    def cards2(self):
        return self.card_set.filter(status=2)
    
    def to_dict(self):
        return {
            'id': self.id,
            'str': str(self),
            'name': self.name,
            'user_id': self.user.id if self.user else None,
            'username': self.user.username if self.user else None,
            'is_ai': self.is_ai,
            'turn': self.turn,
            'cards': [card.to_dict() for card in self.cards],
            'cards1': [card.to_dict() for card in self.cards1],
            'cards2': [card.to_dict() for card in self.cards2],
        }


class Card(models.Model):

    STATUS_CHOICES = (
        (-1, '弃牌'),
        (0, '牌堆'),
        (1, '上场'),
        (2, '休息'),
    )

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    skill = models.ForeignKey(Skill, null=True, blank=True, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return f'{self.player or "野生"}的{self.pokemon}'
    
    def gain_exp(self, exp):
        self.exp += exp
        if self.exp >= self.level * X_LEVEL_UP:
            self.level_up()
        self.save()
        
    def level_up(self):
        self.level += 1
        self.exp = 0
        self.save()

    def action(self, action):
        game = self.game

        assert not game.block
        assert self.player == game.turn_player

        if action == 'learn':
            skill = self.learn()
            game.next_turn()
            return f'{self.pokemon} 学会了技能 {skill}'

        elif action == 'evo':
            evo_card = self.evo()
            if evo_card:
                game.next_turn()
                return f'{self.pokemon} 进化为 {evo_card.pokemon}!'
            return '无法进化，回合继续'

        elif action in ['add_attack', 'defense', 'hp']:
            kind = action[4:]
            if self.available_points > 0:
                self.extrapoint_set.create(kind=kind)
                game.next_turn()
                return f'{self} 增加 1 点 {kind}'

        elif action == 'rest':
            self.status = 2
            self.save()
            return f'{self} 回到精灵中心休息，回合继续'

        elif action == 'join':
            if self.player.cards1.count() < 6:
                self.status = 1
                self.save()
                game.next_turn()
                return f'{self} 上场准备战斗'
            return '上场精灵已满，回合继续'

        return '没有事情发生，回合继续'
        
    def evo(self):
        if not self.can_evo:
            return
        card = self.game.card_set.filter(pokemon=self.pokemon.evo_to, player=None).first()
        assert card, self.id
        card.player = self.player
        card.level = self.level
        card.skill = self.skill
        card.status = self.status
        card.save()
        self.status = -1
        self.player = None
        self.save()
        return card
        
    def learn(self):
        skills = Skill.objects.filter(system__in=self.systems, power__lte=self.level/2)
        if skills:
            skill = random.choice(skills)
        else:
            skill = Skill.objects.filter(system__in=self.systems).order_by('power').first()
        self.skill = skill
        self.save()
        return skill
    
    def to_dict(self):
        return {
            'id': self.id,
            'str': str(self),
            'pokemon': self.pokemon.to_dict(),
            'skill': self.skill.to_dict() if self.skill else None,
            'level': self.level,
            'exp': self.exp,
            'status': self.status,
            'systems': self.systems,
            'attack': self.attack,
            'defense': self.defense,
            'hp': self.hp,
            'effective_points': self.effective_points,
            'available_points': self.available_points,
            'level_up_exp': self.level_up_exp,
        }

    @property
    def can_evo(self):
        if not self.pokemon.evo_to:
            return False
        return self.level >= self.pokemon.evo_to.level
    
    @property
    def systems(self):
        return self.pokemon.system.split('/')

    @property
    def attack(self):
        extra_points = self.extrapoint_set.filter(kind='attack').count()
        return self.pokemon.attack + extra_points

    @property
    def defense(self):
        extra_points = self.extrapoint_set.filter(kind='defense').count()
        return self.pokemon.defense + extra_points

    @property
    def hp(self):
        extra_points = self.extrapoint_set.filter(kind='hp').count()
        return self.pokemon.hp + extra_points

    @property
    def effective_points(self):
        return self.extrapoint_set.all().count()

    @property
    def available_points(self):
        return self.level - self.pokemon.level - self.effective_points
    
    @property
    def level_up_exp(self):
        return self.level * X_LEVEL_UP
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.skill:
            self.learn()


class ExtraPoint(models.Model):

    KIND_CHOICES = (
        ('attack', 'attack'),
        ('defense', 'defense'),
        ('hp', 'hp'),
    )

    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default='attack')

    def __str__(self):
        return f'{self.card}+{self.kind}'
    

def get_harm(card1, card2):
    x = 1
    for system in card2.systems:
        print(card1.skill.system, system)
        y = SYSTEM_MAP[card1.skill.system][system]
        if y > x:
            x = y
        
    if random.randint(1, 5) == 1:
        # 五分之一几率被闪避
        harm = 0
        text = f'{card1} 使用 {card1.skill} 攻击 {card2}，没有命中。'
    else:
        harm = card1.attack + card1.skill.power * x - card2.defense
        harm = max(harm, 1)
        xt = st = ''
        if random.randint(1, 5) == 1:
            # 五分之一几率致命一击
            harm *= 2
            st = '，致命一击'
        if x == 0:
            xt = '，技能无效'
        elif x == 0.5:
            xt = '，效果一般'
        elif x == 2:
            xt = '，效果拔群'
        text = f'{card1} 使用 {card1.skill} 攻击 {card2}，造成 {harm} 点伤害{st}{xt}。'
        
    return harm, text
    

class Battle(models.Model):
    card1 = models.ForeignKey(Card, null=True, blank=True, related_name='card1_battle_set', on_delete=models.CASCADE)
    card2 = models.ForeignKey(Card, null=True, blank=True, related_name='card2_battle_set', on_delete=models.CASCADE)
    events = models.TextField(blank=True)
    winner = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.card1} vs {self.card2}'
    
    @property
    def game(self):
        return self.card1.game
    
    @property
    def winner_card(self):
        if self.winner == 1:
            return self.card1
        elif self.winner == 2:
            return self.card2
        else:
            return None
    
    @property
    def loser_card(self):
        if self.winner == 1:
            return self.card2
        elif self.winner == 2:
            return self.card1
        else:
            return None
        
    @property
    def texts(self):
        return self.events.strip().splitlines()
    
    def fight(self):
        assert not self.events, self.id
        turn = True
        hp1 = self.card1.hp
        hp2 = self.card2.hp
        while not self.winner:
            if turn:
                harm, text = get_harm(self.card1, self.card2)
                hp2 -= harm
                self.events += text + '\n'
            else:
                harm, text = get_harm(self.card2, self.card1)
                hp1 -= harm
                self.events += text + '\n'
            if hp2 <= 0:
                self.winner = 1
                self.events += f'{self.card1} 获胜！'
            elif hp1 <= 0:
                self.winner = 2
                self.events += f'{self.card2} 获胜！'
            turn = not turn
        self.save()
        return self.winner_card
    
    def to_dict(self):
        return {
            'id': self.id,
            'str': str(self),
            'card1': self.card1.to_dict() if self.card1 else None,
            'card2': self.card2.to_dict() if self.card2 else None,
            'texts': self.texts,
            'winner': self.winner,
            'winner_card': self.winner_card.to_dict() if self.winner_card else None,
            'loser_card': self.loser_card.to_dict() if self.loser_card else None,
        }


class Match(models.Model):
    
    player1 = models.ForeignKey(Player, related_name='player1_match_set', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='player2_match_set', on_delete=models.CASCADE)
    winner = models.IntegerField(default=0)
    events = models.TextField(blank=True)
    battles = models.ManyToManyField(Battle)
    
    def __str__(self):
        return f'{self.player1} VS {self.player1}'
    
    @property
    def step(self):
        if self.battles.filter(card1__isnull=False, card2__isnull=False, winner=0).exists():
            return 0, f'正在战斗'
        if not self.player2.cards1.exists():
            return 1, f'{self.player1} 获得胜利！'
        if not self.player1.cards1.exists():
            return 2, f'{self.player2} 获得胜利！'
        if self.battles.filter(card1__isnull=False, card2__isnull=True).exists():
            return 3, f'等待 {self.player2} 选择出战精灵'
        return 4, f'等待 {self.player1} 选择出战精灵'
    
    @property
    def step_code(self):
        return self.step[0]
    
    @property
    def step_display(self):
        return self.step[1]
    
    @property
    def battle_list(self):
        return self.battles.order_by('id')
    
    @property
    def game(self):
        return self.player1.game
    
    @property
    def winner_player(self):
        if self.winner == 1:
            return self.player1
        elif self.winner == 2:
            return self.player2
        else:
            return None
    
    @property
    def loser_player(self):
        if self.winner == 1:
            return self.player2
        elif self.winner == 2:
            return self.player1
        else:
            return None

    @property
    def texts(self):
        return self.events.strip().splitlines()

    def fight(self, card):
        assert card.status == 1
        assert card.game == self.game
        player = card.player
        if player == self.player1:
            assert self.step_code == 4
            self.battles.create(card1=card)
        elif player == self.player2:
            assert self.step_code == 3
            battle = self.battles.order_by('-id').first()
            assert not battle.card2
            battle.card2 = card
            battle.save()
            battle.fight()

            if battle.winner == 1:
                self.events += f'{battle.card1} 战胜 {battle.card2}\n'

                total_exp = battle.card2.attack + battle.card2.defense + battle.card2.hp
                remain_cards = self.player1.card_set.filter(status=1).exclude(id=battle.card1.id)
                remain_count = remain_cards.count()
                if remain_count <= 0:
                    battle.card1.gain_exp(total_exp)
                    self.events += f'{battle.card1.pokemon} 获得 {total_exp} 经验值\n'
                else:
                    battle.card1.gain_exp(total_exp / 2)
                    self.events += f'{battle.card1.pokemon} 获得 {total_exp / 2} 经验值\n'
                    for c in remain_cards:
                        c.gain_exp(total_exp / 2 / remain_count)
                        self.events += f'{c.pokemon} 获得 {total_exp / 2 / remain_count} 经验值\n'

                self.events += f'{battle.card2} 进入精灵中心休息\n'
                battle.card2.status = 2
                battle.card2.save()

            elif battle.winner == 2:
                self.events += f'{battle.card2} 战胜 {battle.card1}\n'

                total_exp = battle.card1.attack + battle.card1.defense + battle.card1.hp
                remain_cards = self.player2.card_set.filter(status=1).exclude(id=battle.card2.id)
                remain_count = remain_cards.count()
                if remain_count <= 0:
                    battle.card2.gain_exp(total_exp)
                    self.events += f'{battle.card2.pokemon} 获得 {total_exp} 经验值\n'
                else:
                    battle.card2.gain_exp(total_exp / 2)
                    self.events += f'{battle.card2.pokemon} 获得 {total_exp / 2} 经验值\n'
                    for c in remain_cards:
                        c.gain_exp(total_exp / 2 / remain_count)
                        self.events += f'{c.pokemon} 获得 {total_exp / 2 / remain_count} 经验值\n'

                self.events += f'{battle.card1} 进入精灵中心休息\n'
                battle.card1.status = 2
                battle.card1.save()

            else:
                assert False
        else:
            assert False

    def to_dict(self):
        return {
            'id': self.id,
            'str': str(self),
            'category': 'match',
            'player1': self.player1.to_dict(),
            'player2': self.player2.to_dict(),
            'winner': self.winner,
            'battles': [b.to_dict for b in self.battle_list],
            'winner_player': self.winner_player.to_dict() if self.winner_player else None,
            'loser_player': self.loser_player.to_dict() if self.loser_player else None,
            'texts': self.texts,
            'step': self.step,
            'step_code': self.step_code,
            'step_display': self.step_display,
        }


class Wild(models.Model):
    
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    winner = models.IntegerField(default=0)
    events = models.TextField(blank=True)
    battles = models.ManyToManyField(Battle)
    
    def __str__(self):
        return f'{self.player} Vs {self.card}'

    @property
    def battle_list(self):
        return self.battles.order_by('id')
    
    @property
    def game(self):
        return self.player.game
    
    @property
    def is_win(self):
        return self.winner == 1

    @property
    def texts(self):
        return self.events.strip().splitlines()

    @property
    def step(self):
        if self.battles.filter(winner=0).exists():
            return 0, f'正在战斗'
        if self.winner == -1:
            return 1, f'{self.player} 逃跑了'
        if self.winner == 1:
            return 2, f'{self.player} 获得胜利！'
        if self.winner == 2:
            return 3, f'{self.player} 被打败了'
        assert not self.battles.exists()
        return 4, f'等待 {self.player} 选择出战精灵'

    @property
    def step_code(self):
        return self.step[0]

    @property
    def step_display(self):
        return self.step[1]
    
    def fight(self, card=None):
        player = self.player
        game = self.game
        assert player == game.turn_player
        if card:
            battle = Battle.objects.create(card1=card, card2=self.card)
            battle.fight()
            self.battles.add(battle)
            self.winner = battle.winner
            self.save()
            if self.is_win:
                wild_card = self.card
                self.events += f'战胜 {wild_card}\n'

                total_exp = wild_card.attack + wild_card.defense + wild_card.hp
                remain_cards = player.card_set.filter(status=1).exclude(id=card.id)
                remain_count = remain_cards.count()
                if remain_count <= 0:
                    card.gain_exp(total_exp)
                    self.events += f'{card.pokemon} 获得 {total_exp} 经验值\n'
                else:
                    card.gain_exp(total_exp / 2)
                    self.events += f'{card.pokemon} 获得 {total_exp / 2} 经验值\n'
                    for c in remain_cards:
                        c.gain_exp(total_exp / 2 / remain_count)
                        self.events += f'{c.pokemon} 获得 {total_exp / 2 / remain_count} 经验值\n'

                if random.randint(1, 5) == 1:
                    # 五分之一几率捕获精灵
                    wild_card.player = player
                    wild_card.status = 1
                    wild_card.save()
                    self.events += f'捕获了 {wild_card.pokemon}!\n'

            else:
                self.events += f'战斗失败，{card} 进入精灵中心休息\n'
                card.status = 2
                card.save()
        else:
            self.winner = -1
            self.save()
            self.events += f'{self.player} 逃跑了\n'

        self.save()
        game.next_turn()

    def to_dict(self):
        return {
            'id': self.id,
            'str': str(self),
            'category': 'wild',
            'player': self.player.to_dict(),
            'card': self.card.to_dict(),
            'winner': self.winner,
            'battles': [b.to_dict for b in self.battle_list],
            'texts': self.texts,
            'is_win': self.is_win,
            'step': self.step,
            'step_code': self.step_code,
            'step_display': self.step_display,
        }