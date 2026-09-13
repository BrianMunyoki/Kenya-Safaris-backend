from rest_framework import serializers

from .models import FAQ, Page, PageSection, PageSectionItem


class PageSectionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageSectionItem
        fields = [
            "id",
            "title",
            "subtitle",
            "content",
            "label",
            "value",
            "icon",
            "image_url",
            "image_alt",
            "link_label",
            "link_url",
            "order",
        ]


class PageSectionSerializer(serializers.ModelSerializer):
    items = PageSectionItemSerializer(many=True, read_only=True)

    class Meta:
        model = PageSection
        fields = [
            "id",
            "section_key",
            "kicker",
            "heading",
            "content",
            "image",
            "image_url",
            "image_alt",
            "link_label",
            "link_url",
            "order",
            "items",
        ]


class PageSerializer(serializers.ModelSerializer):
    sections = PageSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = [
            "id",
            "slug",
            "title",
            "subtitle",
            "hero_image",
            "hero_image_url",
            "hero_image_alt",
            "hero_tag",
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
