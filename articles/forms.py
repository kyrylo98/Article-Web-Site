from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title", "description", "image",
            "body", "is_published",
        ]
        widgets = {
            "description": forms.TextInput(
                attrs={"maxlength": 160}
            ),
            "image": forms.ClearableFileInput(
                attrs={"accept": "image/*"}
            ),
            "body": forms.Textarea(attrs={"rows": 12}),
        }
