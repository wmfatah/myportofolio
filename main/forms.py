from django.forms import ModelForm, TextInput, Textarea, URLInput
from main.models import Experience, Project


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

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]
        labels = {
            "title": "Judul Experience",
            "description": "Deskripsi",
            "category": "Kategori",
            "thumbnail": "URL Thumbnail",
            "ended_at": "Tanggal Selesai",
        }
        widgets = {
            "title": TextInput(attrs={
                "placeholder": "Judul experience",
                "maxlength": 255,
            }),
            "description": Textarea(attrs={
                "placeholder": "Ceritakan pengalamanmu",
                "rows": 3,
            }),
            "thumbnail": URLInput(attrs={
                "placeholder": "https://example.com/image.jpg",
            }),
        }