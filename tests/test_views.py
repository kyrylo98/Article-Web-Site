from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from articles.models import Article
from category.models import Category

User = get_user_model()


class ArticleViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username="author", password="pass12345"
        )
        cls.other_user = User.objects.create_user(
            username="other", password="pass12345"
        )
        cls.staff_user = User.objects.create_user(
            username="staff", password="pass12345", is_staff=True
        )

        cls.category_backend = Category.objects.create(name="Backend")
        cls.category_frontend = Category.objects.create(name="Frontend")
# comment removed (non-English)
        for index in range(7):
            Article.objects.create(
                title=f"Post {index}",
                description="Desc",
                body="text body",
                author=cls.author,
                is_published=True,
                published_at=timezone.now(),
                category=(
                    cls.category_backend
                    if index % 2 == 0
                    else cls.category_frontend
                ),
            )
# comment removed (non-English)
        Article.objects.create(
            title="Draft",
            description="Hidden",
            body="nope",
            author=cls.author,
            is_published=False,
        )

    def test_index_status_and_template(self):
        response = self.client.get(reverse("articles:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/list.html")

    def test_index_shows_only_published(self):
        response = self.client.get(reverse("articles:index"))
        titles = [article.title for article in response.context["page_obj"]]
        self.assertNotIn("Draft", titles)

    def test_index_pagination_second_page(self):
        response_page1 = self.client.get(reverse("articles:index"))
        self.assertEqual(
            response_page1.context["page_obj"].paginator.per_page, 6
        )
        response_page2 = self.client.get(
            reverse("articles:index") + "?page=2"
        )
        self.assertEqual(response_page2.status_code, 200)
        self.assertEqual(
            len(response_page2.context["page_obj"].object_list), 1
        )

    def test_index_search_by_title(self):
        url = reverse("articles:index") + "?search=Post 1"
        response = self.client.get(url)
        objects = list(response.context["page_obj"].object_list)
        self.assertTrue(objects)
        self.assertTrue(any("Post 1" in a.title for a in objects))

    def test_index_filter_by_category(self):
        url = (
            reverse("articles:index")
            + f"?category={self.category_backend.pk}"
        )
        response = self.client.get(url)
        objects = list(response.context["page_obj"].object_list)
        self.assertTrue(objects)
        self.assertTrue(
            all(a.category_id == self.category_backend.pk for a in objects)
        )

    def test_detail_status_ok(self):
        article = Article.objects.filter(is_published=True).first()
        response = self.client.get(
            reverse("articles:detail", args=[article.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/detail.html")

    def test_create_requires_login(self):
        response = self.client.get(reverse("articles:create"))
        self.assertEqual(response.status_code, 302)

    def test_create_sets_author(self):
        self.client.force_login(self.author)
        data = {
            "title": "New Post",
            "description": "Short",
            "body": "Some text",
            "is_published": True,
            "category": self.category_backend.pk,
        }
        response = self.client.post(
            reverse("articles:create"), data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        created = Article.objects.get(title="New Post")
        self.assertEqual(created.author_id, self.author.id)

    def test_update_forbidden_for_non_author(self):
        article = Article.objects.filter(is_published=True).first()
        self.client.force_login(self.other_user)
        old_title = article.title
        response = self.client.post(
            reverse("articles:edit", args=[article.pk]),
            {"title": "Hack"},
            follow=True,
        )
        article.refresh_from_db()
        self.assertEqual(article.title, old_title)
        self.assertIn(response.status_code, (200, 302, 403))

    def test_update_allowed_for_author(self):
        article = Article.objects.filter(is_published=True).first()
        self.client.force_login(self.author)
        data = {
            "title": "Edited",
            "description": "Desc",
            "body": "Body",
            "is_published": True,
            "category": self.category_frontend.pk,
        }
        response = self.client.post(
            reverse("articles:edit", args=[article.pk]),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        article.refresh_from_db()
        self.assertEqual(article.title, "Edited")
        self.assertEqual(
            article.category_id, self.category_frontend.pk
        )

    def test_delete_allowed_for_staff(self):
        article = Article.objects.filter(is_published=True).first()
        self.client.force_login(self.staff_user)
        response = self.client.post(
            reverse("articles:delete", args=[article.pk]),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Article.objects.filter(pk=article.pk).exists())


