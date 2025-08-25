# category/context_processors.py
from django.db.models import Count
from .models import Category

def nav_categories(request):
    items = (
        Category.objects.annotate(article_count=Count("articles"))
        .order_by("-article_count", "name")[:12]
    )
    return {"nav_categories": items}

