from rest_framework import serializers

from .models import ContactEnquiry, TripEnquiry


class ContactEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactEnquiry
        fields = ["id", "name", "email", "phone", "subject", "message", "created_at"]
        read_only_fields = ["id", "created_at"]


class TripEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripEnquiry
        fields = [
            "id", "name", "email", "phone", "preferred_dates", "guests", "notes",
            "destinations", "duration", "budget", "safari_type", "created_at",
        ]
        read_only_fields = ["id", "created_at"]
