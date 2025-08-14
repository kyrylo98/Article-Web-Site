from django.db import models
from django.conf import settings
from articles.models import Article
from comments.models import Comment


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "article", "comment")

    def __str__(self):
        target = self.article or self.comment
        return f"{self.user} liked {target}"
