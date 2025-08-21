from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def home_view(request):
    if request.user.is_authenticated:
        return redirect("users:account")
    return render(request, "index.html")
