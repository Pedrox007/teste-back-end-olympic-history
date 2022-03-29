from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from core.serializers import AthleteSerializer, TeamSerializer, ModalitySerializer, SportSerializer, GameSerializer

from core.models import Athlete, Team, Modality, Sport, Game


class AthleteViewSet(viewsets.ModelViewSet):
    serializer_class = AthleteSerializer
    queryset = Athlete.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "name",
        "age",
        "height",
        "weight",
        "gender",
        "team__name",
        "team__noc",
        "participation__medal",
        "participation__game__year",
        "participation__game__season",
        "participation__game__city",
        "participation__modality__sport__name",
        "participation__modality__description"
    ]


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "noc"]


class ModalityViewSet(viewsets.ModelViewSet):
    serializer_class = ModalitySerializer
    queryset = Modality.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["description", "sport__name"]


class SportViewSet(viewsets.ModelViewSet):
    serializer_class = SportSerializer
    queryset = Sport.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["season", "year", "city"]
