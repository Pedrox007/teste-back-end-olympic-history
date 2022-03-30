from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from core.models import Team, Participation, Game, Modality, Sport, Athlete


class ModalityTestCase(APITestCase):

    def setUp(self):
        self.sport = Sport.objects.create(name="Sport")

        self.modality = Modality.objects.create(description="Modality", sport=self.sport)

    def tearDown(self):
        self.sport.delete()
        self.modality.delete()

    def test_get_modality_by_id(self):
        url = f"/modality/{self.modality.id}/"
        api_response = self.client.get(url, format="json")

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(api_response.data["description"], "Modality")

    def test_get_modality_with_filter(self):
        url = f"/modality/?description={self.modality.description}"
        api_response = self.client.get(url)

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(api_response.json()["results"]), 1)

    def test_create_modality(self):
        url = f"/modality/"
        api_response = self.client.post(url, {"description": "New Modality", "sport_id": self.sport.id})

        self.assertEqual(api_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(api_response.json()["description"], "New Modality")

    def test_edit_modality(self):
        url = f"/modality/{self.modality.id}/"
        api_response = self.client.put(url, {"description": "ModalityEdit", "sport_id": self.sport.id})

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(api_response.json()["description"], "ModalityEdit")

    def test_del_modality(self):
        url = f"/modality/{self.modality.id}/"
        api_response = self.client.delete(url)

        self.assertEqual(api_response.status_code, status.HTTP_204_NO_CONTENT)
