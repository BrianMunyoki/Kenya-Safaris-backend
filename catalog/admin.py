from django.contrib import admin

from .models import Destination, SafariPackage


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "tag", "is_published", "order")
    list_editable = ("is_published", "order")
    list_filter = ("is_published", "tag")
    search_fields = ("title", "subtitle", "overview", "tag")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SafariPackage)
class SafariPackageAdmin(admin.ModelAdmin):
    list_display = ("title", "destination", "price_label", "badge", "is_published", "order")
    list_editable = ("is_published", "order")
    list_filter = ("is_published", "destination", "badge")
    search_fields = ("title", "subtitle", "overview", "tag")
    prepopulated_fields = {"slug": ("title",)}
