from django.forms import ModelForm, TextInput, Textarea, URLInput
from main.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "technology",
            "project_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "technology": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
        }

        widgets = {
            "title": TextInput(attrs={
                "placeholder": "Nama proyek",
                "maxlength": 255,
            }),

            "description": Textarea(attrs={
                "placeholder": "Ceritakan proyekmu",
                "rows": 3,
            }),

            "technology": TextInput(attrs={
                "placeholder": "Django, Python, HTML, CSS",
            }),

            "project_url": URLInput(attrs={
                "placeholder": "https://example.com",
            }),
        }