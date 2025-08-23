from django.db.models import Count
from .models import Category

def nav_categories(request):
    return {
        "nav_categories": (
            Category.objects
            .annotate(article_count=Count("articles"))
            .order_by("name")
        )
    }
