from django.contrib import admin

from .models import ContactEnquiry, TripEnquiry


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "subject", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)


@admin.register(TripEnquiry)
class TripEnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "guests", "preferred_dates", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "notes")
    readonly_fields = ("created_at",)
