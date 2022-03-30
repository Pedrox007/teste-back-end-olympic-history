from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from core.models import Team, Participation, Game, Modality, Sport, Athlete


class CoreTestCase(APITestCase):

    def setUp(self):
        self.team = Team.objects.create(name="Team", noc="TEA")

    def tearDown(self):
        self.team.delete()

    def test_get_team(self):
        url = f"/team/{self.team.id}/"
        api_response = self.client.get(url, format="json")

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(api_response.data["name"], "Team")

    def test_get_team_with_filter(self):
        url = f"/team/?name={self.team.name}"
        api_response = self.client.get(url)

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(api_response.json()["results"]), 1)

    def test_create_team(self):
        url = f"/team/"
        api_response = self.client.post(url, {"name": "NewTeam", "noc": "NEW"})

        self.assertEqual(api_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(api_response.json()["name"], "NewTeam")

    def test_edit_team(self):
        url = f"/team/{self.team.id}/"
        api_response = self.client.put(url, {"name": "TeamEdit", "noc": "TED"})

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(api_response.json()["name"], "TeamEdit")

    def test_del_team(self):
        url = f"/team/{self.team.id}/"
        api_response = self.client.delete(url)

        self.assertEqual(api_response.status_code, status.HTTP_204_NO_CONTENT)
