from rest_framework import serializers

from .models import (
    Destination,
    SafariPackage,
    SafariFAQ,
)


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = [
            "id",
            "name",
            "slug",
            "tag",
            "description",
            "image",
            "highlights",
            "order",
        ]


class SafariFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafariFAQ
        fields = [
            "id",
            "question",
            "answer",
            "order",
        ]


class SafariPackageSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)

    highlights = serializers.SerializerMethodField()
    itinerary = serializers.SerializerMethodField()
    includes = serializers.SerializerMethodField()
    excludes = serializers.SerializerMethodField()
    related_links = serializers.SerializerMethodField()

    faqs = serializers.SerializerMethodField()

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

            "seo_title",
            "meta_description",

            "highlights",
            "itinerary",
            "includes",
            "excludes",
            "related_links",
            "faqs",

            "badge",
            "order",
        ]

    def get_highlights(self, obj):
        return [
            item.text
            for item in obj.highlight_items.all()
        ]

    def get_itinerary(self, obj):
        return [
            {
                "day": item.day,
                "title": item.title,
                "desc": item.description,
            }
            for item in obj.itinerary_days.all()
        ]

    def get_includes(self, obj):
        return [
            item.text
            for item in obj.include_items.all()
        ]

    def get_excludes(self, obj):
        return [
            item.text
            for item in obj.exclude_items.all()
        ]

    def get_related_links(self, obj):
        return [
            {
                "label": item.label,
                "to": item.url,
            }
            for item in obj.related_link_items.all()
        ]

    def get_faqs(self, obj):
        faqs = getattr(obj, "published_faqs", [])

        return SafariFAQSerializer(
            faqs,
            many=True,
        ).data