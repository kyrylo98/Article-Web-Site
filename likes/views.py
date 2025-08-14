from rest_framework import viewsets
from .models import Article
from .serializers import LikeSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = LikeSerializer
