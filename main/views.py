from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import ExperienceForm, ProjectForm
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
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    projects = [project.object for project in projects]

    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Muhammad Fatahillah Widodo",
        "project_list": projects,
        "title_query": title_query,
    }

    return render(request, "projects.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Muhammad Fatahillah Widodo",
        "form": form,
    }

    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()

    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)

    return HttpResponse(
        projects_json,
        content_type="application/json"
    )   

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Muhammad Fatahillah Widodo",
        "page_title": "Tambah Experience",
        "form": form,   
    }

    return render(request, "experience_form.html", context)

def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    form = ExperienceForm(
        request.POST or None,
        instance=experience
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Muhammad Fatahillah Widodo",
        "page_title": "Edit Experience",
        "form": form,
    }

    return render(request, "experience_form.html", context)