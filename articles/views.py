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


class HomeListView(ListView):
    model = Article
    template_name = "articles/list.html"
    context_object_name = "articles"
    paginate_by = 6

    def get_queryset(self):
        articles_queryset = (
            Article.objects.filter(is_published=True)
            .select_related("author", "category")
        )

        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            articles_queryset = articles_queryset.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(body__icontains=search_query)
            )

        category_id = self.request.GET.get("category", "").strip()
        if category_id.isdigit():
            articles_queryset = articles_queryset.filter(
                category_id=category_id
            )

        return articles_queryset.order_by("-published_at", "-pk")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["active_category"] = self.request.GET.get("category", "")
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


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
