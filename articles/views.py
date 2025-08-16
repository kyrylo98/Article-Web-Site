from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .forms import ArticleForm
from .models import Article, Category, Tag


class ArticleListView(ListView):
    template_name = "articles/article_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        qs = Article.objects.select_related("author", "category").prefetch_related(
            "tags"
        )
        category_slug = self.request.GET.get("category")
        tag_slug = self.request.GET.get("tag")
        search = self.request.GET.get("q")

        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if tag_slug:
            qs = qs.filter(tags__slug=tag_slug)
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(
                content__icontains=search
            )
        return qs

    def article_list(request):
        articles = Article.objects.all()
        return render(request, "articles/article_list.html", {"articles": articles})


class ArticleDetailView(DetailView):
    template_name = "articles/article_detail.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Article.objects.select_related("author", "category").prefetch_related(
                "tags"
            ),
            slug=self.kwargs["slug"],
            is_published=True,
        )


class AuthorOrStaffRequired(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or obj.author_id == self.request.user.id


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/article_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, AuthorOrStaffRequired, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/article_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class ArticleDeleteView(LoginRequiredMixin, AuthorOrStaffRequired, DeleteView):
    model = Article
    success_url = reverse_lazy("articles:article_list")
    template_name = "articles/article_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
