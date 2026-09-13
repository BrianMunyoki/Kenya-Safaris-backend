from django.contrib import admin

from .models import (
    Destination,
    SafariPackage,
    SafariHighlight,
    SafariItineraryDay,
    SafariInclude,
    SafariExclude,
    SafariRelatedLink,
    SafariFAQ,
)


class SafariHighlightInline(admin.TabularInline):
    model = SafariHighlight
    extra = 1
    fields = ("text", "order")


class SafariItineraryDayInline(admin.StackedInline):
    model = SafariItineraryDay
    extra = 0
    fields = (
        "day",
        "title",
        "description",
        "order",
    )


class SafariIncludeInline(admin.TabularInline):
    model = SafariInclude
    extra = 1
    fields = ("text", "order")


class SafariExcludeInline(admin.TabularInline):
    model = SafariExclude
    extra = 1
    fields = ("text", "order")


class SafariRelatedLinkInline(admin.TabularInline):
    model = SafariRelatedLink
    extra = 1
    fields = (
        "label",
        "url",
        "order",
    )


class SafariFAQInline(admin.StackedInline):
    model = SafariFAQ
    extra = 1
    fields = (
        "question",
        "answer",
        "order",
        "is_published",
    )


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tag",
        "is_published",
        "order",
    )

    list_editable = (
        "is_published",
        "order",
    )

    list_filter = (
        "is_published",
        "tag",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(SafariPackage)
class SafariPackageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "destination",
        "duration",
        "price_label",
        "badge",
        "is_published",
        "order",
    )

    list_editable = (
        "is_published",
        "order",
    )

    list_filter = (
        "is_published",
        "destination",
        "badge",
    )

    search_fields = (
        "title",
        "subtitle",
        "overview",
        "seo_title",
        "meta_description",
        "tag",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    fieldsets = (
        (
            "Basic information",
            {
                "fields": (
                    "title",
                    "slug",
                    "destination",
                    "subtitle",
                    "tag",
                    "badge",
                )
            },
        ),
        (
            "Safari details",
            {
                "fields": (
                    "duration",
                    "price_label",
                    "group_size",
                    "difficulty",
                )
            },
        ),
        (
            "Image",
            {
                "fields": (
                    "image",
                    "image_alt",
                )
            },
        ),
        (
            "Main content",
            {
                "fields": (
                    "overview",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "seo_title",
                    "meta_description",
                )
            },
        ),
        (
            "Publishing",
            {
                "fields": (
                    "is_published",
                    "order",
                )
            },
        ),
    )

    inlines = (
        SafariHighlightInline,
        SafariItineraryDayInline,
        SafariIncludeInline,
        SafariExcludeInline,
        SafariRelatedLinkInline,
        SafariFAQInline,
    )