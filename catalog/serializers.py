from rest_framework import serializers

from .models import Destination, SafariPackage


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = [
            "id", "name", "slug", "tag", "description", "image",
            "highlights", "order",
        ]


class SafariPackageSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)

    class Meta:
        model = SafariPackage
        fields = [
            "id",
            "title",
            "slug",
            "destination",
            "subtitle",
            "tag",
            "image",
            "image_alt",
            "duration",
            "price_label",
            "group_size",
            "difficulty",
            "overview",
            "highlights",
            "itinerary",
            "includes",
            "excludes",
            "related_links",
            "badge",
            "order",
        ]