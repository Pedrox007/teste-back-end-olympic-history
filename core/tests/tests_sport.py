from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from core.models import Team, Participation, Game, Modality, Sport, Athlete


class TeamTestCase(APITestCase):

    def setUp(self):
        self.sport = Sport.objects.create(name="Sport")

    def tearDown(self):
        self.sport.delete()

    def test_get_sport(self):
        url = f"/sport/{self.sport.id}/"
        api_response = self.client.get(url, format="json")

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(api_response.data["name"], "Sport")

    def test_get_sport_with_filter(self):
        url = f"/sport/?name={self.sport.name}"
        api_response = self.client.get(url)

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(api_response.json()["results"]), 1)

    def test_create_sport(self):
        url = f"/sport/"
        api_response = self.client.post(url, {"name": "NewSport"})

        self.assertEqual(api_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(api_response.json()["name"], "NewSport")

    def test_edit_sport(self):
        url = f"/sport/{self.sport.id}/"
        api_response = self.client.put(url, {"name": "SportEdit"})

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(api_response.json()["name"], "SportEdit")

    def test_del_sport(self):
        url = f"/sport/{self.sport.id}/"
        api_response = self.client.delete(url)

        self.assertEqual(api_response.status_code, status.HTTP_204_NO_CONTENT)