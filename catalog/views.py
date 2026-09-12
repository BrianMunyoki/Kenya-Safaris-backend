from rest_framework import generics

from .models import Destination, SafariPackage
from .serializers import DestinationSerializer, SafariPackageSerializer


class DestinationListView(generics.ListAPIView):
    """GET /api/catalog/destinations/"""
    queryset = Destination.objects.filter(is_published=True)
    serializer_class = DestinationSerializer


class DestinationDetailView(generics.RetrieveAPIView):
    """GET /api/catalog/destinations/<slug>/"""
    queryset = Destination.objects.filter(is_published=True)
    serializer_class = DestinationSerializer
    lookup_field = "slug"


class SafariPackageListView(generics.ListAPIView):
    """GET /api/catalog/packages/  (optional ?destination=<slug> filter)"""
    serializer_class = SafariPackageSerializer

    def get_queryset(self):
        qs = SafariPackage.objects.filter(is_published=True)
        destination_slug = self.request.query_params.get("destination")
        if destination_slug:
            qs = qs.filter(destination__slug=destination_slug)
        return qs


class SafariPackageDetailView(generics.RetrieveAPIView):
    """GET /api/catalog/packages/<slug>/"""
    queryset = SafariPackage.objects.filter(is_published=True)
    serializer_class = SafariPackageSerializer
    lookup_field = "slug"
