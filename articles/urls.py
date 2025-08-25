from django.urls import path

from .views import (ArticleCreateView, ArticleDeleteView, ArticleDetailView,
                    ArticleUpdateView, HomeListView)

app_name = "articles"

urlpatterns = [
    path("", HomeListView.as_view(), name="index"),
    path("create/", ArticleCreateView.as_view(), name="create"),
    path("<int:pk>/", ArticleDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", ArticleUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name="delete"),
]

