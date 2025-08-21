from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username", "email", "is_staff",
        "is_verified", "rating",
    )
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Profile", {
            "fields": ("avatar", "bio", "rating", "is_verified")
        }),
    )
