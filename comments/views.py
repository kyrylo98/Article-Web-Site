from rest_framework import viewsets
from .models import Article
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = CommentSerializer
