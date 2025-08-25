from django.urls import path
from django.views.generic import TemplateView

app_name = "pages"

urlpatterns = [
    path("about/", TemplateView.as_view(
        template_name="pages/about.html"), name="about"),
    path("blog/", TemplateView.as_view(
        template_name="pages/blog.html"), name="blog"),
    path("contact/", TemplateView.as_view(
        template_name="pages/contact.html"), name="contact"),
    path("privacy/", TemplateView.as_view(
        template_name="pages/privacy.html"), name="privacy"),
    path("terms/", TemplateView.as_view(
        template_name="pages/terms.html"), name="terms"),
    path("cookies/", TemplateView.as_view(
        template_name="pages/cookies.html"), name="cookies"),
    path("sitemap/", TemplateView.as_view(
        template_name="pages/sitemap.html"), name="sitemap"),
]

