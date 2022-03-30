from django.db import transaction
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
    sport_id = serializers.PrimaryKeyRelatedField(queryset=Sport.objects.all(), source="sport", write_only=True)

    class Meta:
        model = Modality
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    season = serializers.ChoiceField(choices=Game.SEASON_CHOICES, write_only=True)
    season_display = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = "__all__"

    def get_season_display(self, instance: Game):
        return instance.get_season_display()


class ParticipationSerializer(serializers.ModelSerializer):
    medal = serializers.ChoiceField(choices=Participation.MEDAL_CHOICES, allow_null=True, write_only=True)
    medal_display = serializers.SerializerMethodField()

    class Meta:
        model = Participation
        fields = "__all__"

    def get_medal_display(self, instance: Participation):
        return instance.get_medal_display()


class NestedParticipationSerializer(ParticipationSerializer):
    id = serializers.IntegerField(required=False)
    game = GameSerializer(read_only=True)
    modality = ModalitySerializer(read_only=True)
    game_id = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all(), source="game", write_only=True)
    modality_id = serializers.PrimaryKeyRelatedField(queryset=Modality.objects.all(), source="modality", write_only=True)

    class Meta:
        model = Participation
        exclude = ("athlete",)


class AthleteSerializer(serializers.ModelSerializer):
    participations = NestedParticipationSerializer(source='participation_set', many=True)
    team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source="team", write_only=True)
    team = TeamSerializer(read_only=True)
    gender = serializers.ChoiceField(choices=Athlete.GENDER_CHOICES, allow_null=True, write_only=True)
    gender_display = serializers.SerializerMethodField()

    class Meta:
        model = Athlete
        exclude = ("game",)

    def get_gender_display(self, instance: Athlete):
        return instance.get_gender_display()

    def validate(self, attrs):
        if not attrs.get("team", None):
            raise serializers.ValidationError("The team's id is necessary.")

        if not attrs.get("name", None):
            raise serializers.ValidationError("The athlete's name is necessary.")

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        participation = validated_data.pop("participation_set", None)
        obj = super().create(validated_data)

        if not participation:
            return obj

        serializer = ParticipationSerializer(
            data=[{
                "medal": data.get("medal", None),
                "athlete": obj.id,
                "game": data["game"].id,
                "modality": data["modality"].id
            } for data in participation],
            many=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError as errors:
            raise serializers.ValidationError({"participation": errors.detail})

        return obj

    @transaction.atomic
    def update(self, instance, validated_data):
        participation = validated_data.pop("participation_set", None)
        instance = super().update(instance, validated_data)

        if not participation:
            return instance

        participation_ids = [data["id"] for data in participation if "id" in data]
        # Delete items
        instance.participation_set.exclude(id__in=participation_ids).delete()

        # Update or create order items
        errors = []
        for i, data in enumerate(participation):
            participation_id = data.pop("id", None)
            try:
                participation_item = Participation.objects.get(id=participation_id)
                s = ParticipationSerializer(
                    instance=participation_item,
                    data={
                        "medal": data.get("medal", None),
                        "athlete": instance.id,
                        "game": data["game"].id,
                        "modality": data["modality"].id
                    }
                )
                s.is_valid(raise_exception=True)
                s.save()
            except Participation.DoesNotExist:
                if participation_id is None:
                    try:
                        s = ParticipationSerializer(data={
                            "medal": data.get("medal", None),
                            "athlete": instance.id,
                            "game": data["game"].id,
                            "modality": data["modality"].id
                        })
                        s.is_valid(raise_exception=True)
                        s.save()
                    except serializers.ValidationError as err:
                        errors.append(err.detail)
                    else:
                        errors.append({})
                else:
                    errors.append({"id": "Participation does not exist."})
            except serializers.ValidationError as err:
                errors.append(err.detail)
            else:
                errors.append({})

        if any([len(e) for e in errors]):
            raise serializers.ValidationError({"items": errors})

        return instance
