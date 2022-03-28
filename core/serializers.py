from rest_framework import serializers

from core.models import Athlete, Team, Participation, Modality, Sport, Game


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = "__all__"


class SportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sport
        fields = "__all__"


class ModalitySerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)

    class Meta:
        model = Modality
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    season = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = "__all__"

    def get_season(self, instance: Game):
        return instance.get_season_display()


class ParticipationSerializer(serializers.ModelSerializer):
    medal_display = serializers.SerializerMethodField()
    game_id = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all(), source="game", write_only=True)
    game = GameSerializer(read_only=True)
    modality_id = serializers.PrimaryKeyRelatedField(queryset=Modality.objects.all(), source="modality", write_only=True)
    modality = ModalitySerializer(read_only=True)

    class Meta:
        model = Participation
        fields = ("id", "medal", "medal_display", "modality", "game", "modality_id", "game_id")

    def get_medal_display(self, instance: Participation):
        return instance.get_medal_display()


class AthleteSerializer(serializers.ModelSerializer):
    participations = ParticipationSerializer(source='participation_set', many=True)
    team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source="team", write_only=True)
    team = TeamSerializer(read_only=True)
    gender = serializers.SerializerMethodField()

    class Meta:
        model = Athlete
        exclude = ("game",)

    def get_gender(self, instance: Athlete):
        return instance.get_gender_display()
