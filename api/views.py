from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import Place
from .serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def list(self, request, *args, **kwargs):
        places = self.queryset
        serializer = self.serializer_class(places, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        place = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(place, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        place = get_object_or_404(self.queryset, pk=pk)
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def nearest_place(self, request):
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")

        if lat is None or lon is None:
            return Response(
                {"error": "Latitude and longitude parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        point = Point(float(lon), float(lat), srid=4326)
        nearest_place = (
            self.queryset.annotate(distance=Distance("geom", point))
            .order_by("distance")
            .first()
        )

        if nearest_place is None:
            return Response(
                {"error": "No places found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(nearest_place)
        return Response(serializer.data)
