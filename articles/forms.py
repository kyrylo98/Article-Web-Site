# articles/forms.py
from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "description", "image", "body", "is_published", "category")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "input", "placeholder": "Awesome headline"
            }),
            "description": forms.TextInput(attrs={
                "class": "input", "placeholder": "Short summary (≤ 160 char)"
            }),
            "body": forms.Textarea(attrs={
                "class": "textarea", "placeholder": "Write your article..."
            }),
            "category": forms.Select(attrs={"class": "select"}),
        }

