from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "author",
        "is_published", "published_at",
    )
    list_filter = ("is_published", "published_at")
    search_fields = ("title", "description", "body")
