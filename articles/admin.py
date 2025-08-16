from django.contrib import admin
from .models import Article, Category, Tag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "is_published", "created_at")
    list_filter = ("is_published", "category", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("tags",)
    date_hierarchy = "created_at"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

