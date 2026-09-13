from rest_framework import serializers

from .models import FAQ, Page, PageSection


class PageSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageSection
        fields = [
            "id",
            "heading",
            "content",
            "image",
            "image_alt",
            "order",
        ]


class PageSerializer(serializers.ModelSerializer):
    sections = PageSectionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Page
        fields = [
            "id",
            "slug",
            "title",
            "subtitle",
            "hero_image",
            "body",
            "sections",
            "updated_at",
        ]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            "id",
            "question",
            "answer",
            "order",
        ]