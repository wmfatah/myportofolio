from django.shortcuts import render
from main.models import Experience, Project


def show_main(request):
    context = { 
        "name": "Muhammad Fatahillah Widodo",
        "npm": "2506623925",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan teknologi."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Muhammad Fatahillah Widodo",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_projects(request):
    context = {
        "name": "Muhammad Fatahillah Widodo",
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)