from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Place


class PlaceTests(APITestCase):
    def setUp(self) -> None:
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

    def test_retrieve_all_places(self) -> None:
        url = reverse("api:place-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_place(self) -> None:
        url = reverse("api:place-list")
        data = {
            "name": "New Place",
            "description": "New Description",
            "geom": "SRID=4326;POINT(3 3)",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 3)

    def test_retrieve_specific_place(self) -> None:
        url = reverse("api:place-detail", args=[self.place1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.place1.name)

    def test_update_place(self) -> None:
        url = reverse("api:place-detail", args=[self.place1.pk])
        data = {"name": "Updated Place"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Place.objects.get(pk=self.place1.pk).name, "Updated Place"
        )

    def test_delete_place(self) -> None:
        url = reverse("api:place-detail", args=[self.place1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Place.objects.count(), 1)

    def test_find_nearest_place(self) -> None:
        url = reverse("api:place-nearest-place")
        params = {"latitude": 1, "longitude": 1}
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.place1.name)

        invalid_params = {"latitude": "invalid", "longitude": "invalid"}
        response = self.client.get(url, invalid_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
