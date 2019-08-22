from django.db import models


class Skill(models.Model):

    name = models.CharField(max_length=50, blank=True)
    system = models.CharField(max_length=10, blank=True)
    cost = models.IntegerField(default=1)
    power = models.IntegerField(default=0)
    buff = models.CharField(max_length=100, blank=True)
    debuff = models.CharField(max_length=100, blank=True)


class Mon(models.Model):

    name = models.CharField(max_length=50, blank=True)
    system = models.CharField(max_length=20, blank=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    mp = models.IntegerField(default=0)
    evolution_to = models.ForeignKey('self', on_delete=models.CASCADE)
    evolution_level = models.IntegerField(default=100)


class Player(models.Model):

    name = models.CharField(max_length=50, blank=True)


class Playmon(models.Model):

    STATUS_CHOICES = (
        (0, '休养'),
        (1, '待命'),
        (2, '上场'),
    )

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mon = models.ForeignKey(Mon, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    mp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    @property
    def systems(self):
        return self.mon.system.split(' ')

    def save(self, *args, **kwargs):
        assert self.player and self.mon
        if not self.id:
            self.attack = self.mon.attack
            self.defense = self.mon.defense
            self.speed = self.mon.speed
            self.hp = self.mon.hp
            self.mp = self.mon.mp
        super().save(*args, **kwargs)
        self.skills.add(self.mon.skill)
