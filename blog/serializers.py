from rest_framework import serializers

from .models import BlogPost


class BlogPostListSerializer(serializers.ModelSerializer):
    read_time = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ["id", "title", "slug", "tag", "excerpt", "hero_image", "read_time", "published_at"]

    def get_read_time(self, obj):
        return f"{obj.read_time_minutes} min read"


class BlogPostDetailSerializer(BlogPostListSerializer):
    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + ["body", "author", "updated_at"]
