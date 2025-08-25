from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count, QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Category
from articles.models import Article


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Доступ только для staff-пользователей."""
    def test_func(self) -> bool:
        return bool(self.request.user and self.request.user.is_staff)


class CategoryListView(ListView):
    """Список категорий с поиском и счётчиком статей."""
    model = Category
    template_name = "categories/list.html"
    context_object_name = "categories"
    paginate_by = 30

    def get_queryset(self) -> QuerySet:
        search_query = self.request.GET.get("q", "").strip()
        category_queryset = Category.objects.annotate(
            article_count=Count("articles")
        ).order_by("name")
        if search_query:
            category_queryset = category_queryset.filter(name__icontains=search_query)
        return category_queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("q", "").strip()
        return context


class CategoryArticlesView(ListView):
    """
    Список статей в категории (вместо DetailView, чтобы было удобно пагинировать).
    """
    template_name = "categories/detail.html"
    context_object_name = "articles"
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        self.category_instance = get_object_or_404(Category, pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        article_queryset = (
            Article.objects.filter(
                category=self.category_instance,
                is_published=True,
            )
            .select_related("author", "category")
            .order_by("-published_at")
        )
        return article_queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["category"] = self.category_instance
        return context


class CategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    fields = ["name", "description"]
    template_name = "categories/form.html"
    success_url = reverse_lazy("categories:index")

    # чтобы шаблон мог обращаться к переменной "category"
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.setdefault("category", None)
        return context


class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    model = Category
    fields = ["name", "description"]
    template_name = "categories/form.html"
    context_object_name = "category"
    success_url = reverse_lazy("categories:index")


class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = Category
    template_name = "categories/confirm_delete.html"
    context_object_name = "category"
    success_url = reverse_lazy("categories:index")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from articles.models import Article  # поправь импорт под свой путь

@login_required
def account_view(request):
    my_articles = (
        Article.objects
        .filter(author=request.user)
        .order_by('-created_at')
    )
    return render(request, 'users/account.html', {
        'my_articles': my_articles,
    })