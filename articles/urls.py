from django.urls import path

from articles.views import index

urlpatterns = [
    path("", index, name="index"),
]
