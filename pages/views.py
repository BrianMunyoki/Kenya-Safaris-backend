from rest_framework import generics

from .models import FAQ, Page
from .serializers import FAQSerializer, PageSerializer


class PageDetailView(generics.RetrieveAPIView):
    """GET /api/pages/<slug>/"""
    queryset = Page.objects.filter(is_published=True)
    serializer_class = PageSerializer
    lookup_field = "slug"


class FAQListView(generics.ListAPIView):
    """GET /api/pages/faqs/"""
    queryset = FAQ.objects.filter(is_published=True)
    serializer_class = FAQSerializer
