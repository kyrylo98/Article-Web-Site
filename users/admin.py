from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("avatar", "bio", "rating", "is_verified")}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Дополнительная информация", {
            "fields": ("avatar", "bio", "rating", "is_verified"),
        }),
    )

    list_display = (
        "id", "username", "email", "is_staff", "is_active",
        "rating", "is_verified", "date_joined"
    )
    list_filter = ("is_staff", "is_active", "is_verified")
    search_fields = ("username", "email")
    ordering = ("id",)
