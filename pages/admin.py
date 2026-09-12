from django.contrib import admin

from .models import FAQ, Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "updated_at")
    list_editable = ("is_published",)
    search_fields = ("title", "slug", "body")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "is_published")
    list_editable = ("order", "is_published")
    search_fields = ("question", "answer")
