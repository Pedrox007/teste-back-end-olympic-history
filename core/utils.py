from django.core.exceptions import ObjectDoesNotExist
from tqdm import tqdm
from core.models import (
    Athlete,
    Team,
    Modality,
    Sport,
    Participation,
    Game
)


def populate_tables(csv_rows):
    csv_rows.sort(key=lambda x: x[0])

    for i, row in zip(tqdm(range(len(csv_rows)), desc="Loading"), csv_rows):
        team_obj = get_team_obj(row)
        athlete_obj = get_athlete_obj(row, team_obj)
        sport_obj = get_sport_obj(row)
        modality_obj = get_modality_obj(row, sport_obj)
        game_obj = get_game_obj(row)
        create_participation_obj(row, athlete_obj, modality_obj, game_obj)


def get_team_obj(row):
    try:
        obj = Team.objects.get(name=row[6], noc=row[7])
    except ObjectDoesNotExist:
        obj = Team(name=row[6], noc=row[7])
        obj.save()

    return obj


def get_athlete_obj(row, team_obj):
    age = row[3] if row[3] != "NA" else None
    height = row[4] if row[4] != "NA" else None
    weight = row[5] if row[5] != "NA" else None
    try:
        obj = Athlete.objects.get(
            name=row[1],
            gender=row[2],
            team=team_obj,
            age=age,
            height=height,
            weight=weight
        )
    except ObjectDoesNotExist:
        obj = Athlete(
            name=row[1],
            gender=row[2],
            team=team_obj,
            age=age,
            height=height,
            weight=weight
        )
        obj.save()

    return obj


def get_sport_obj(row):
    try:
        obj = Sport.objects.get(name=row[12])
    except ObjectDoesNotExist:
        obj = Sport(name=row[12])
        obj.save()

    return obj


def get_modality_obj(row, sport_obj):
    try:
        obj = Modality.objects.get(description=row[13], sport=sport_obj)
    except ObjectDoesNotExist:
        obj = Modality(description=row[13], sport=sport_obj)
        obj.save()

    return obj


def get_game_obj(row):
    try:
        obj = Game.objects.get(year=row[9], season=row[10][0])
    except ObjectDoesNotExist:
        obj = Game(year=row[9], season=row[10][0], city=row[11])
        obj.save()

    return obj


def create_participation_obj(row, athlete_obj, modality_obj, game_obj):
    medal = row[-1][0] if row[-1] != "NA" else None
    try:
        obj = Participation.objects.get(athlete=athlete_obj, modality=modality_obj, game=game_obj, medal=medal)
    except ObjectDoesNotExist:
        obj = Participation(athlete=athlete_obj, modality=modality_obj, game=game_obj, medal=medal)
        obj.save()

    return obj
