from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from Article_Web_Site.views import home_view

urlpatterns = [
    path("admin/", admin.site.urls),

    # Главная (лендинг/индекс)
    path("", home_view, name="home"),

    # Статьи и пользователи
    path("articles/", include(("articles.urls", "articles"),
                              namespace="articles")),
    path("users/", include(("users.urls", "users"), namespace="users")),

    # Аутентификация (шаблоны из папки templates/registration/)
    path("login/",
         auth_views.LoginView.as_view(
             template_name="registration/login.html"
         ),
         name="login"),
    path("logout/",
         auth_views.LogoutView.as_view(),
         name="logout"),

    # Смена пароля (готовые представления Django)
    path("password-change/",
         auth_views.PasswordChangeView.as_view(
             template_name="registration/password_change_form.html"
         ),
         name="password_change"),
    path("password-change/done/",
         auth_views.PasswordChangeDoneView.as_view(
             template_name="registration/password_change_done.html"
         ),
         name="password_change_done"),
    path("categories/", include("category.urls", namespace="categories")),
    path("", include(("pages.urls", "pages"), namespace="pages")),

    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)


