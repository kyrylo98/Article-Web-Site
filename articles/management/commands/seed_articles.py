# articles/management/commands/seed_articles.py
from __future__ import annotations

import random
import textwrap

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from articles.models import Article


LOREM_SENTENCES = [
    "Shipping faster is about saying no to the wrong features.",
    "Small teams with clear goals beat committees every time.",
    "Write docs first, code second, polish last.",
    "Bugs love silence; logs and tests make them visible.",
    "Release notes are for people, not for robots.",
    "Naming is hard; pick clear words and keep them short.",
    "Delete dead code. Future you will send thanks.",
    "Latency is a feature. Treat it as a design problem.",
    "Your default state should be boring and reliable.",
    "Start with text, not pixels. Structure wins.",
    "Automate repeated pain; scripts are cheap insurance.",
    "Great UX removes choices until only one remains.",
    "Measure before you optimize; guesses are expensive.",
    "A migration plan is part of the feature, not extra.",
    "Security is a habit, not a milestone.",
    "Write changelogs that read like a story.",
    "Prefer constraints over conventions when it matters.",
    "Caching hides sins; monitor and invalidate with care.",
    "Backups you never restore do not exist.",
    "Every alert should be actionable or be deleted.",
]

TITLE_PART_A = [
    "Practical", "Modern", "Tiny", "Calm", "Opinionated", "Readable",
    "Bulletproof", "Elegant", "Everyday", "Minimal", "Quiet", "Effective",
]

TITLE_PART_B = [
    "Django Patterns", "Release Notes", "API Design", "Code Reviews",
    "Migrations", "Onboarding", "Testing", "Logging", "CLI Tools",
    "Docs", "Background Jobs", "Caching",
]


def make_title(i: int) -> str:
    a = random.choice(TITLE_PART_A)
    b = random.choice(TITLE_PART_B)
    return f"{a} {b} #{i}"


def make_body() -> str:
    pick = random.sample(LOREM_SENTENCES, k=8)
    paras = [" ".join(pick[:4]), " ".join(pick[4:])]
    body = "\n\n".join(paras)
    return textwrap.fill(body, width=78)


def make_description(body: str) -> str:
    one_line = " ".join(body.split())
    if len(one_line) <= 160:
        return one_line
    return one_line[:157] + "..."


class Command(BaseCommand):
    help = "Seed the database with demo articles."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--count",
            type=int,
            default=20,
            help="How many articles to create (default: 20).",
        )
        parser.add_argument(
            "--wipe",
            action="store_true",
            help="Delete all existing articles first.",
        )

    def handle(self, *args, **opts) -> None:
        count: int = opts["count"]
        wipe: bool = opts["wipe"]

        if wipe:
            deleted, _ = Article.objects.all().delete()
            self.stdout.write(f"Deleted {deleted} rows.")

        User = get_user_model()
        author = (
            User.objects.filter(is_superuser=True).first()
            or User.objects.filter(is_staff=True).first()
            or User.objects.first()
        )
        if not author:
            author = User.objects.create_user(
                username="writer",
                email="writer@example.com",
                password="writer12345",
            )
            self.stdout.write("Created fallback user 'writer'.")

        created = 0
        for i in range(1, count + 1):
            title = make_title(i)
            body = make_body()
            desc = make_description(body)

            article = Article(
                title=title,
                description=desc,
                body=body,
                author=author,
                is_published=random.choice([True, False, True]),
            )
# comment removed (non-English)
            if hasattr(article, "published_at"):
                shift = random.randint(-30, 0)
                article.published_at = timezone.now() + timezone.timedelta(
                    days=shift
                )

            article.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} articles."))


