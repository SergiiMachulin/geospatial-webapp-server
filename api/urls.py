from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import PlaceViewSet

router = SimpleRouter()
router.register("places", PlaceViewSet, basename="place")


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "api"
