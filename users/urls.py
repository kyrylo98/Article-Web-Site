from django.urls import path

from .views import account_view

app_name = "users"

urlpatterns = [
    path("account/", account_view, name="account"),
]
