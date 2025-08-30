from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from .forms import ProfileUpdateForm


@login_required
def account_view(request):
    return render(request, "users/account.html")


@login_required
def profile_update_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("users:account")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(
        request, "users/profile_form.html", {"form": form}
    )


class AccountPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("users:account")


