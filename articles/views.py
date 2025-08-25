from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin,
)
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from category.models import Category
from .forms import ArticleForm
from .models import Article


# articles/views.py
class HomeListView(ListView):
    model = Article
    template_name = "articles/list.html"
    context_object_name = "articles"
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        qs = Article.objects.select_related("author", "category")

        author_param = (self.request.GET.get("author") or "").strip().lower()
        if author_param == "me" and user.is_authenticated:
            qs = qs.filter(author_id=user.id)                       # свои (можно и неопубликованные)
        elif author_param.isdigit():
            author_id = int(author_param)
            if user.is_authenticated and author_id == user.id:
                qs = qs.filter(author_id=user.id)                   # свои
            else:
                qs = qs.filter(author_id=author_id, is_published=True)  # чужие только опубликованные
        else:
            qs = qs.filter(is_published=True)

        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(description__icontains=q) | Q(body__icontains=q)
            )

        cat = (self.request.GET.get("category") or "").strip()
        if cat.isdigit():
            qs = qs.filter(category_id=cat)

        return qs.order_by("-published_at", "-pk")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        author_param = (self.request.GET.get("author") or "").strip().lower()

        is_my = author_param == "me" or (
            author_param.isdigit() and user.is_authenticated and int(author_param) == user.id
        )

        ctx.update({
            "categories": Category.objects.all(),
            "active_category": (self.request.GET.get("category") or "").strip(),
            "search_query": (self.request.GET.get("q") or "").strip(),
            "is_my_articles": is_my,
        })
        return ctx

class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.select_related("author", "category")


class AuthorRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        article = self.get_object()
        current_user = self.request.user
        return (
            current_user.is_staff
            or (
                current_user.is_authenticated
                and article.author_id == current_user.id
            )
        )


class ArticleCreateView(LoginRequiredMixin,
                        CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("articles:detail", args=(self.object.pk,))


class ArticleUpdateView(LoginRequiredMixin,
                        AuthorRequiredMixin,
                        UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/form.html"

    def get_success_url(self):
        return reverse("articles:detail", args=(self.object.pk,))


class ArticleDeleteView(LoginRequiredMixin,
                        AuthorRequiredMixin,
                        DeleteView):
    model = Article
    template_name = "articles/confirm_delete.html"
    success_url = reverse_lazy("articles:index")
