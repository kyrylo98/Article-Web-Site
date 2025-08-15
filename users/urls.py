from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.index, name="index"),
    path("like/<int:article_id>/", views.like_article, name="like_article"),
    path("comment/<int:article_id>/", views.add_comment, name="add_comment"),
    path("users/", views.users_list, name="users_list"),
]
