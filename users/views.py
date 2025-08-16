from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from articles.models import Article
from comments.models import Comment
from likes.models import Like


User = get_user_model()
def index(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'articles': articles})


@login_required
def like_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    like, created = Like.objects.get_or_create(article=article, user=request.user)

    if not created:
        like.delete()

    return redirect("index")


@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == "POST":
        text = request.POST.get("text")
        if text.strip():
            Comment.objects.create(article=article, author=request.user, content=text)
    return redirect("index")


def users_list(request):
    users = User.objects.all()
    return render(request, "users.html", {"users": users})

