from django.contrib import admin

from .models import FAQ, Page, PageSection


class PageSectionInline(admin.StackedInline):
    model = PageSection
    extra = 0

    fields = (
        "heading",
        "content",
        "image",
        "image_alt",
        "order",
    )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "is_published",
        "updated_at",
    )

    list_editable = (
        "is_published",
    )

    search_fields = (
        "title",
        "slug",
        "body",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    inlines = [
        PageSectionInline,
    ]


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = (
        "heading",
        "page",
        "order",
    )

    list_filter = (
        "page",
    )

    list_editable = (
        "order",
    )

    search_fields = (
        "heading",
        "content",
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "order",
        "is_published",
    )

    list_editable = (
        "order",
        "is_published",
    )

    search_fields = (
        "question",
        "answer",
    )