from rest_framework import viewsets

from core.serializers import AthleteSerializer, TeamSerializer, ModalitySerializer, SportSerializer, GameSerializer

from core.models import Athlete, Team, Modality, Sport, Game


class AthleteViewSet(viewsets.ModelViewSet):
    serializer_class = AthleteSerializer
    queryset = Athlete.objects.all().order_by("id")


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all().order_by("id")


class ModalityViewSet(viewsets.ModelViewSet):
    serializer_class = ModalitySerializer
    queryset = Modality.objects.all().order_by("id")


class SportViewSet(viewsets.ModelViewSet):
    serializer_class = SportSerializer
    queryset = Sport.objects.all().order_by("id")


class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all().order_by("id")
