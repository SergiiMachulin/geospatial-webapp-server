from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from api.views import PlaceViewSet

router = routers.DefaultRouter()
router.register(r"places", PlaceViewSet)

schema_view = get_swagger_view(title="Geospatial API")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/docs/", schema_view),
]
