from rest_framework import generics, permissions

from .models import ContactEnquiry, TripEnquiry
from .serializers import ContactEnquirySerializer, TripEnquirySerializer


class ContactEnquiryCreateView(generics.CreateAPIView):
    """POST /api/leads/contact/  - what the Contact page form submits to."""
    queryset = ContactEnquiry.objects.all()
    serializer_class = ContactEnquirySerializer
    permission_classes = [permissions.AllowAny]


class TripEnquiryCreateView(generics.CreateAPIView):
    """POST /api/leads/plan-my-trip/  - what the Plan My Trip wizard submits to."""
    queryset = TripEnquiry.objects.all()
    serializer_class = TripEnquirySerializer
    permission_classes = [permissions.AllowAny]
