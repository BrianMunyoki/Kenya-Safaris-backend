from django.db.models import Prefetch
from rest_framework import generics

from .models import (
    Destination,
    SafariPackage,
    SafariFAQ,
)
from .serializers import (
    DestinationSerializer,
    SafariPackageSerializer,
)


class DestinationListView(generics.ListAPIView):
    queryset = Destination.objects.filter(is_published=True)
    serializer_class = DestinationSerializer


class DestinationDetailView(generics.RetrieveAPIView):
    queryset = Destination.objects.filter(is_published=True)
    serializer_class = DestinationSerializer
    lookup_field = "slug"


class SafariPackageListView(generics.ListAPIView):
    serializer_class = SafariPackageSerializer

    def get_queryset(self):
        qs = (
            SafariPackage.objects
            .filter(is_published=True)
            .select_related("destination")
            .prefetch_related(
                "highlight_items",
                "itinerary_days",
                "include_items",
                "exclude_items",
                "related_link_items",
                Prefetch(
                    "faqs",
                    queryset=SafariFAQ.objects.filter(is_published=True),
                    to_attr="published_faqs",
                ),
            )
        )

        destination_slug = self.request.query_params.get("destination")

        if destination_slug:
            qs = qs.filter(destination__slug=destination_slug)

        return qs


class SafariPackageDetailView(generics.RetrieveAPIView):
    serializer_class = SafariPackageSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            SafariPackage.objects
            .filter(is_published=True)
            .select_related("destination")
            .prefetch_related(
                "highlight_items",
                "itinerary_days",
                "include_items",
                "exclude_items",
                "related_link_items",
                Prefetch(
                    "faqs",
                    queryset=SafariFAQ.objects.filter(is_published=True),
                    to_attr="published_faqs",
                ),
            )
        )