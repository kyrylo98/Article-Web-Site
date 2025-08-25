from django.conf import settings
from django.db import models
from django.urls import reverse

from category.models import Category


def article_image_path(instance, filename) -> str:
    prefix = instance.pk or "new"
    return f"articles/{prefix}/{filename}"


class Article(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=160)
    body = models.TextField()
    image = models.ImageField(
        upload_to=article_image_path, blank=True, null=True
    )
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles",

    )
    category = models.ForeignKey(
        Category,
        verbose_name="Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )

    class Meta:
        ordering = ["-published_at"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("articles:detail", kwargs={"pk": self.pk})

    @property
    def reading_minutes(self) -> int:
        words = len(self.body.split())
        return max(1, words // 200)

