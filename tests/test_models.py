from django.test import TestCase
from django.contrib.auth import get_user_model
from articles.models import Article

User = get_user_model()


class ArticleModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="author",
            password="pass12345",
        )

    def test_str_returns_title(self):
        article = Article.objects.create(
            title="My Title",
            description="Desc",
            body="Body text",
            author=self.user,
        )
        self.assertEqual(str(article), "My Title")

    def test_reading_minutes_min_1(self):
        article = Article.objects.create(
            title="Short",
            description="Desc",
            body="one two",
            author=self.user,
        )
        self.assertEqual(article.reading_minutes, 1)

    def test_reading_minutes_counts_words(self):
        words = " ".join(["word"] * 600)
        article = Article.objects.create(
            title="Long",
            description="Desc",
            body=words,
            author=self.user,
        )
        self.assertEqual(article.reading_minutes, 3)

