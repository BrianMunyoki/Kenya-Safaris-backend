from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "read_time_minutes", "is_published", "published_at", "order")
    list_editable = ("is_published", "order")
    list_filter = ("is_published", "tag")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("published_at", "updated_at")
