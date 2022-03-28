from django.contrib import admin

from core.models import Team, Athlete, Modality, Sport, Game, Participation


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "noc")
    ordering = ("id",)


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age", "height", "weight", "team_id")
    ordering = ("id",)


@admin.register(Modality)
class ModalityAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "sport_id")
    ordering = ("id",)


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    ordering = ("id",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "year", "season", "city")
    ordering = ("id",)


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("id", "athlete_id", "modality_id", "game_id", "medal")
    ordering = ("id",)
