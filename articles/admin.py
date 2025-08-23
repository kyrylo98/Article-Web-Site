from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "author", "category",
        "published_at", "is_published"
    )
    list_filter = ("is_published", "published_at", "category" )
    search_fields = ("title", "description", "body")
