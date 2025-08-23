from django.urls import path
from . import views
from .views import CategoryListView

app_name = "categories"

urlpatterns = [
    path("", views.categories_list_view, name="index"),
    path("<int:pk>/", views.category_detail_view, name="detail"),
    path("create/", views.category_create_view, name="create"),
    path("<int:pk>/edit/", views.category_edit_view, name="edit"),
    path("<int:pk>/delete/", views.category_delete_view, name="delete"),
    path("", CategoryListView.as_view(), name="list")
]
