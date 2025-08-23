from django.test import SimpleTestCase
from django.urls import reverse, resolve
from articles.views import (
    HomeListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
)


class ArticleUrlTests(SimpleTestCase):
    def test_index_url(self):
        url = reverse("articles:index")
        self.assertEqual(resolve(url).func.view_class, HomeListView)

    def test_detail_url(self):
        url = reverse("articles:detail", args=[1])
        self.assertEqual(resolve(url).func.view_class, ArticleDetailView)

    def test_create_url(self):
        url = reverse("articles:create")
        self.assertEqual(resolve(url).func.view_class, ArticleCreateView)

    def test_update_url(self):
        url = reverse("articles:edit", args=[1])
        self.assertEqual(resolve(url).func.view_class, ArticleUpdateView)

    def test_delete_url(self):
        url = reverse("articles:delete", args=[1])
        self.assertEqual(resolve(url).func.view_class, ArticleDeleteView)
