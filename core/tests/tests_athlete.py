from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from core.models import Team, Participation, Game, Modality, Sport, Athlete


class CoreTestCase(APITestCase):

    def setUp(self):
        self.team = Team.objects.create(name="Team", noc="TEA")

        self.athlete = Athlete.objects.create(name="Athlete", age=20, height=1.70, weight=70, gender="M", team=self.team)

        self.sport = Sport.objects.create(name="Sport")

        self.modality = Modality.objects.create(description="Modality", sport=self.sport)

        self.game = Game.objects.create(year=2000, season="S", city="Natal")

        self.participation = Participation.objects.create(medal="G", athlete=self.athlete, game=self.game, modality=self.modality)

    def tearDown(self):
        self.athlete.delete()
        self.team.delete()
        self.sport.delete()
        self.modality.delete()
        self.game.delete()
        self.participation.delete()

    def test_get_Athlete(self):
        url = f"/athlete/{self.athlete.id}/"
        api_response = self.client.get(url, format="json")

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(api_response.data["name"], "Athlete")

    def test_get_athlete_with_filter(self):
        url = f"/athlete/?name={self.athlete.name}"
        api_response = self.client.get(url)

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(api_response.json()["results"]), 1)

    def test_create_athlete(self):
        url = f"/athlete/"
        api_response = self.client.post(url, {
            "name": "New Athlete",
            "age": 20,
            "height": 1.8,
            "weight": 70,
            "gender": "F",
            "team_id": self.team.id,
            "participations": [
                {
                    "medal": "G",
                    "modality_id": self.modality.id,
                    "game_id": self.game.id
                },
                {
                    "medal": "S",
                    "modality_id": self.modality.id,
                    "game_id": self.game.id
                }
            ]
        })

        self.assertEqual(api_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(api_response.json()["name"], "New Athlete")

    def test_edit_athlete(self):
        url = f"/athlete/{self.athlete.id}/"
        api_response = self.client.put(url, {
            "name": "AthleteEdit",
            "age": 20,
            "height": 1.70,
            "weight": 70,
            "gender": "M",
            "team_id": self.team.id,
            "participations": []
        })

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(api_response.json()["name"], "AthleteEdit")

    def test_del_athlete(self):
        url = f"/athlete/{self.athlete.id}/"
        api_response = self.client.delete(url)

        self.assertEqual(api_response.status_code, status.HTTP_204_NO_CONTENT)
