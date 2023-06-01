from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Place


class PlaceTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.list_url = reverse("api:place-list")
        cls.detail_url = lambda pk: reverse("api:place-detail", args=[pk])
        cls.nearest_place_url = reverse("api:place-nearest-place")

    def setUp(self):
        self.place1 = Place.objects.create(
            name="Place 1",
            description="Description 1",
            geom="SRID=4326;POINT(1 1)",
        )
        self.place2 = Place.objects.create(
            name="Place 2",
            description="Description 2",
            geom="SRID=4326;POINT(2 2)",
        )

    def test_retrieve_all_places(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_place(self):
        data = {
            "name": "New Place",
            "description": "New Description",
            "geom": "SRID=4326;POINT(3 3)",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 3)

    def test_retrieve_specific_place(self):
        response = self.client.get(self.detail_url(self.place1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.place1.name)

    def test_update_place(self):
        data = {"name": "Updated Place"}
        response = self.client.put(self.detail_url(self.place1.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Place.objects.get(pk=self.place1.pk).name, "Updated Place")

    def test_delete_place(self):
        response = self.client.delete(self.detail_url(self.place1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Place.objects.count(), 1)

    def test_find_nearest_place(self):
        params = {"latitude": 1, "longitude": 1}
        response = self.client.get(self.nearest_place_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.place1.name)

        invalid_params = {"latitude": "invalid", "longitude": "invalid"}
        response = self.client.get(self.nearest_place_url, invalid_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
