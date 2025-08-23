from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .models import Category
from articles.models import Article


def categories_list_view(request):
    query = request.GET.get("q", "").strip()
    qs = Category.objects.all()
    if query:
        qs = qs.filter(name__icontains=query)

    paginator = Paginator(qs, 20)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    return render(
        request,
        "categories/list.html",
        {"page_obj": page_obj, "query": query},
    )


def category_detail_view(request, pk: int):
    category = get_object_or_404(Category, pk=pk)
    qs = Article.objects.filter(
        category=category, is_published=True
    ).order_by("-published_at")

    paginator = Paginator(qs, 10)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    return render(
        request,
        "categories/detail.html",
        {"category": category, "page_obj": page_obj},
    )


@staff_member_required
@require_http_methods(["GET", "POST"])
def category_create_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        if name:
            Category.objects.create(name=name, description=description)
            return redirect("categories:index")
    return render(request, "categories/form.html", {"mode": "create"})


@staff_member_required
@require_http_methods(["GET", "POST"])
def category_edit_view(request, pk: int):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        if name:
            category.name = name
            category.description = description
            category.save(update_fields=["name", "description"])
            return redirect("categories:index")
    return render(
        request, "categories/form.html",
        {"mode": "edit", "category": category},
    )


@staff_member_required
@require_http_methods(["GET", "POST"])
def category_delete_view(request, pk: int):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("categories:index")
    return render(
        request, "categories/confirm_delete.html",
        {"category": category},
    )
