from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().select_related("author", "category").prefetch_related("tags")
    serializer_class = ArticleSerializer
