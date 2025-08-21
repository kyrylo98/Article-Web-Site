from django import forms

from .models import User


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "email",
            "avatar", "bio",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            "avatar": forms.ClearableFileInput(
                attrs={"accept": "image/*"}
            ),
        }
