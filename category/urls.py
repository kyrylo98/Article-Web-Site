from django.urls import path
from .views import (
    CategoryListView,
    CategoryArticlesView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
)

app_name = "categories"

urlpatterns = [
    path("", CategoryListView.as_view(), name="index"),
    path("<int:pk>/", CategoryArticlesView.as_view(), name="detail"),
    path("create/", CategoryCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", CategoryUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", CategoryDeleteView.as_view(), name="delete"),
]
