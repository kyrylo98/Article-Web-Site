from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
)

app_name = "articles"

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("create/", ArticleCreateView.as_view(), name="create"),

    path("<slug:slug>/", ArticleDetailView.as_view(), name="article_detail"),

    path("<slug:slug>/edit/", ArticleUpdateView.as_view(), name="edit"),
    path("<slug:slug>/delete/", ArticleDeleteView.as_view(), name="delete"),
  ]
