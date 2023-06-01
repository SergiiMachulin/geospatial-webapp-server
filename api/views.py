from django.core.exceptions import ValidationError
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
)
from rest_framework import viewsets, status

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Place
from .pagination import PlacePagination
from .serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.order_by("id")
    serializer_class = PlaceSerializer
    pagination_class = PlacePagination

    @extend_schema(
        description="Retrieve a list of places.",
        responses={200: PlaceSerializer(many=True)},
    )
    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Create a new place.",
        request=PlaceSerializer,
        responses={201: PlaceSerializer},
        examples=[
            OpenApiExample(
                name="Example 1 create Place",
                value={
                    "name": "New Place",
                    "description": "Super new",
                    "geom": "SRID=4326;POINT(100 100)",
                },
                response_only=False,
            )
        ],
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Retrieve a single place by ID.",
        responses={200: PlaceSerializer()},
    )
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Update a place by ID.",
        request=PlaceSerializer,
        responses={200: PlaceSerializer()},
    )
    def update(self, request: Request, *args, **kwargs) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(
        description="Partial update of a place by ID.",
        request=PlaceSerializer,
        responses={200: PlaceSerializer()},
    )
    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="Delete a place by ID.",
        responses={204: None},
    )
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="latitude",
                description="Latitude coordinate of the target location.",
                required=True,
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="longitude",
                description="Longitude coordinate of the target location.",
                required=True,
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
            ),
        ],
        description="Find the nearest place to the given coordinates.",
        responses={200: PlaceSerializer()},
        examples=[
            OpenApiExample(
                name="Find nearest place",
                value={"latitude": 1, "longitude": 1},
            )
        ],
    )
    @action(detail=False, methods=["get"])
    def nearest_place(self, request: Request) -> Response:
        try:
            latitude = float(request.query_params.get("latitude"))
            longitude = float(request.query_params.get("longitude"))

        except (ValueError, TypeError):
            raise ValidationError("Invalid latitude or longitude values.")

        point = Point(latitude, longitude, srid=4326)

        nearest_place = (
            Place.objects.annotate(distance=Distance("geom", point))
            .order_by("distance")
            .first()
        )

        serializer = self.get_serializer(nearest_place)
        return Response(serializer.data, status.HTTP_200_OK)
