from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin,
)
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .forms import ArticleForm
from .models import Article


class HomeListView(ListView):
    model = Article
    template_name = "articles/list.html"
    context_object_name = "articles"
    paginate_by = 6

    def get_queryset(self):
        base_queryset = Article.objects.filter(is_published=True)
        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            base_queryset = base_queryset.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(body__icontains=search_query)
            )
        return base_queryset.select_related("author")


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/detail.html"
    context_object_name = "article"


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        article = self.get_object()
        user = self.request.user
        return user.is_staff or (user.is_authenticated and
                                 article.author_id == user.id)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(
    LoginRequiredMixin, AuthorRequiredMixin, UpdateView
):
    model = Article
    form_class = ArticleForm
    template_name = "articles/form.html"


class ArticleDeleteView(
    LoginRequiredMixin, AuthorRequiredMixin, DeleteView
):
    model = Article
    template_name = "articles/confirm_delete.html"
    success_url = reverse_lazy("articles:index")
