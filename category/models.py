from django.db import models


class Category(models.Model):
    name = models.CharField(
        "Name",
        max_length=64,
        unique=True,
    )
    description = models.TextField(
        "Description",
        blank=True,
    )
    created_at = models.DateTimeField(
        "Created at",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
