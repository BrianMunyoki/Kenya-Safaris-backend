from django.contrib import admin

from .models import FAQ, Page, PageSection, PageSectionItem


class PageSectionInline(admin.StackedInline):
    model = PageSection
    extra = 0
    show_change_link = True

    fields = (
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
    )


class PageSectionItemInline(admin.StackedInline):
    model = PageSectionItem
    extra = 0

    fields = (
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
    )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "is_published",
        "updated_at",
    )
    list_editable = ("is_published",)
    search_fields = ("title", "slug", "body")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PageSectionInline]

    fieldsets = (
        ("Page", {
            "fields": ("title", "slug", "subtitle", "body", "is_published"),
        }),
        ("Hero", {
            "fields": (
                "hero_tag",
                "hero_image",
                "hero_image_url",
                "hero_image_alt",
            ),
        }),
    )


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = (
        "heading",
        "section_key",
        "page",
        "order",
    )
    list_filter = ("page", "section_key")
    list_editable = ("order",)
    search_fields = ("heading", "kicker", "content", "section_key")
    inlines = [PageSectionItemInline]


@admin.register(PageSectionItem)
class PageSectionItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "section",
        "order",
    )
    list_filter = ("section__page", "section")
    list_editable = ("order",)
    search_fields = ("title", "subtitle", "content", "label", "value")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "is_published")
    list_editable = ("order", "is_published")
    search_fields = ("question", "answer")
