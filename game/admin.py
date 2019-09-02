from django.contrib import admin

from game import models


@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'system', 'power']
    list_filter = ['system']


@admin.register(models.Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'no', 'system', 'attack', 'defense', 'hp', 'level', 'evo_to']
    raw_id_fields = ['default_skill', 'evo_to']


@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'game', 'user', 'name', 'is_ai', 'turn']
    raw_id_fields = ['game', 'user']
    list_filter = ['game', 'user', 'is_ai']


@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['id', 'game', 'player', 'pokemon', 'skill', 'level', 'status', 'attack', 'defense', 'hp', 'available_points']
    raw_id_fields = ['game', 'player', 'pokemon', 'skill']
    list_filter = ['game']


@admin.register(models.ExtraPoint)
class ExtraPointAdmin(admin.ModelAdmin):
    list_display = ['id', 'card', 'kind']
    list_filter = ['kind']


