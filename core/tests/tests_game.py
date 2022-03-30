from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from core.models import Team, Participation, Game, Modality, Sport, Athlete


class CoreTestCase(APITestCase):

    def setUp(self):
        self.game = Game.objects.create(year=2000, season="S", city="Natal")

    def tearDown(self):
        self.game.delete()

    def test_get_game(self):
        url = f"/game/{self.game.id}/"
        api_response = self.client.get(url, format="json")

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(api_response.data["city"], "Natal")

    def test_get_game_with_filter(self):
        url = f"/game/?city={self.game.city}"
        api_response = self.client.get(url)

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(api_response.json()["results"]), 1)

    def test_create_game(self):
        url = f"/game/"
        api_response = self.client.post(url, {"year": 2022, "season": "W", "city": "São Paulo"})

        self.assertEqual(api_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(api_response.json()["city"], "São Paulo")

    def test_edit_game(self):
        url = f"/game/{self.game.id}/"
        api_response = self.client.put(url, {"year": 2020, "season": "W", "city": "Natal"})

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(api_response.json()["year"], 2020)

    def test_del_game(self):
        url = f"/game/{self.game.id}/"
        api_response = self.client.delete(url)

        self.assertEqual(api_response.status_code, status.HTTP_204_NO_CONTENT)
