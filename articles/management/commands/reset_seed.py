# articles/management/commands/reset_seed.py
import io
import math
import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from PIL import Image, ImageDraw, ImageFont

from articles.models import Article
from category.models import Category
# comment removed (non-English)
CATEGORIES = [
    "News", "Politics", "World", "Business", "Finance",
    "Technology", "Programming", "Python", "Django", "Frontend",
    "Backend", "APIs", "AI", "Machine Learning", "Security",
    "DevOps", "Cloud", "Data Science", "IoT", "Mobile",
    "Cars", "Plants", "Astrology", "UX", "Open Source",
]

ADJ = ["Quick", "Practical", "Modern", "Essential", "Deep",
       "Beginner", "Advanced", "Clean", "Smart", "Pro"]

NOUN = ["Guide", "Checklist", "Patterns", "Tips", "Playbook",
        "Notes", "Snippets", "Workflow", "Plan", "Roadmap"]

BODY = [
    "This article explains the topic with simple steps and examples.",
    "You will find a practical checklist and recommendations.",
    "We focus on clarity, short paragraphs and actionable advice.",
    "Use the patterns to save time in real projects.",
    "Links to further reading are provided at the end.",
]

PALETTES = [
    (("#3b82f6", "#06b6d4"), "#ffffff"),
    (("#22c55e", "#06b6d4"), "#ffffff"),
    (("#a855f7", "#6366f1"), "#ffffff"),
    (("#f59e0b", "#ef4444"), "#0b1220"),
    (("#0ea5e9", "#10b981"), "#0b1220"),
]

def _pick_author():
    User = get_user_model()
    author = User.objects.filter(is_staff=True).first() or User.objects.first()
    if not author:
        author = User.objects.create_user(
            username="seed", email="seed@example.com",
            password="seedpass123", is_staff=True,
        )
    return author

def _font(size=64):
    for name in ("DejaVuSans.ttf", "Arial.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()

def _measure(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int]:
# comment removed (non-English)
    if hasattr(draw, "textbbox"):
        l, t, r, b = draw.textbbox((0, 0), text, font=font)
        return r - l, b - t
    return draw.textsize(text, font=font)  # fallback

def _make_image(text: str, w=1200, h=630) -> ContentFile:
# comment removed (non-English)
    (c1, c2), ink = random.choice(PALETTES)

    def hex2rgb(hex_color: str):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    start = hex2rgb(c1)
    end = hex2rgb(c2)

    img = Image.new("RGB", (w, h), start)
    draw = ImageDraw.Draw(img)
# comment removed (non-English)
    for y in range(h):
        t = y / h
        col = tuple(int(start[i] * (1 - t) + end[i] * t) for i in range(3))
        draw.line([(0, y), (w, y)], fill=col)
# comment removed (non-English)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.rectangle([0, 0, w, h], fill=(0, 0, 0, 40))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
# comment removed (non-English)
    title = text[:28]
    font = _font(74)
    tw, th = _measure(draw, title, font)
    x, y = (w - tw) // 2, (h - th) // 2
# comment removed (non-English)
    for dx, dy in ((2, 2), (1, 1)):
        draw.text((x + dx, y + dy), title, font=font, fill=(0, 0, 0, 120))
# comment removed (non-English)
    draw.text((x, y), title, font=font, fill=ink)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90, optimize=True)
    buf.seek(0)
    return ContentFile(buf.read(), name="cover.jpg")

class Command(BaseCommand):
    help = "Reset demo data: 25 categories + 100 published articles with images."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Deleting old articles…"))
        Article.objects.all().delete()

        self.stdout.write(self.style.WARNING("(Re)creating categories…"))
        Category.objects.all().delete()
        categories = [
            Category.objects.create(
                name=name,
                description=f"{name} — curated posts and practical insights.",
            )
            for name in CATEGORIES
        ]

        author = _pick_author()

        self.stdout.write(self.style.WARNING("Creating 100 articles…"))
        total = 100
        per_cat = total // len(categories)  # 4 на каждую
        created = 0
        now = timezone.now()

        for cat in categories:
            for _ in range(per_cat):
                if created >= total:
                    break
                title = f"{random.choice(ADJ)} {cat.name} {random.choice(NOUN)}"
                desc = f"{cat.name}: a short, actionable overview with examples."[:160]
                body = "\n\n".join(random.sample(BODY, k=3))

                article = Article(
                    title=title,
                    description=desc,
                    body=body,
                    is_published=True,
                    published_at=now - timedelta(days=random.randint(0, 200)),
                    author=author,
                    category=cat,
                )
                image = _make_image(cat.name)
                article.image.save(f"{slugify(cat.name)}-{created+1}.jpg", image, save=False)
                article.save()
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done! Categories: {Category.objects.count()}, Articles: {Article.objects.count()}"
        ))


