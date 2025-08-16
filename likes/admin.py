from django.contrib import admin
from .models import Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "article", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("user__username", "article__title")
    ordering = ("-created_at",)
