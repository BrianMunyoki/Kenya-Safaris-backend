from rest_framework import serializers

from .models import FAQ, Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["id", "slug", "title", "subtitle", "hero_image", "body", "sections", "updated_at"]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["id", "question", "answer", "order"]
