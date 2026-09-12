from rest_framework import generics

from .models import BlogPost
from .serializers import BlogPostDetailSerializer, BlogPostListSerializer


class BlogPostListView(generics.ListAPIView):
    """GET /api/blog/  - powers the Guides & Blog hub"""
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostListSerializer


class BlogPostDetailView(generics.RetrieveAPIView):
    """GET /api/blog/<slug>/  - powers a single article page"""
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostDetailSerializer
    lookup_field = "slug"
