from django.urls import path

from .views import (
    AccountPasswordChangeView,
    account_view,
    profile_update_view,
)

app_name = "users"

urlpatterns = [
    path("account/", account_view, name="account"),
    path("profile/", profile_update_view, name="profile"),
    path(
        "password-change/",
        AccountPasswordChangeView.as_view(),
        name="password_change",
    ),
]
