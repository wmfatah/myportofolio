import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project


def show_main(request):
    last_login = request.COOKIES.get(
        "last_login",
        "Belum ada sesi login / Cookie tidak ditemukan"
    )

    context = {
        "name": "Muhammad Fatahillah Widodo",
        "npm": "2506623925",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan teknologi."
        ),
        "last_login": last_login,
    }

    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experiences_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8")
    )

    experiences = [
        experience.object
        for experience in experiences
    ]

    context = {
        "name": "Muhammad Fatahillah Widodo",
        "experience_list": experiences,
    }

    return render(request, "experience.html", context)


def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(
            title__icontains=title_query
        )

    context = {
        "name": "Muhammad Fatahillah Widodo",
        "project_list": projects,
        "title_query": title_query,
    }

    return render(request, "projects.html", context)


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Proyek baru berhasil ditambahkan!"
        )

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
        projects = projects.filter(
            title__icontains=title_query
        )

    projects_json = serializers.serialize(
        "json",
        projects
    )

    return HttpResponse(
        projects_json,
        content_type="application/json"
    )


@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(
        Project,
        pk=project_id
    )

    if request.method == "POST":
        project.delete()

        messages.success(
            request,
            "Project berhasil dihapus!"
        )

    return redirect("main:show_projects")


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Experience baru berhasil ditambahkan!"
        )

        return redirect("main:show_experience")

    context = {
        "name": "Muhammad Fatahillah Widodo",
        "page_title": "Tambah Experience",
        "form": form,
    }

    return render(
        request,
        "experience_form.html",
        context
    )


def update_experience(request, experience_id):
    experience = get_object_or_404(
        Experience,
        pk=experience_id
    )

    form = ExperienceForm(
        request.POST or None,
        instance=experience
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Experience berhasil diperbarui!"
        )

        return redirect("main:show_experience")

    context = {
        "name": "Muhammad Fatahillah Widodo",
        "page_title": "Edit Experience",
        "form": form,
    }

    return render(
        request,
        "experience_form.html",
        context
    )


def delete_experience(request, experience_id):
    experience = get_object_or_404(
        Experience,
        pk=experience_id
    )

    if request.method == "POST":
        experience.delete()

        messages.success(
            request,
            "Experience berhasil dihapus!"
        )

    return redirect("main:show_experience")


def get_experiences_json(request):
    experiences = Experience.objects.all()

    experiences_json = serializers.serialize(
        "json",
        experiences
    )

    return HttpResponse(
        experiences_json,
        content_type="application/json"
    )


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Akun berhasil dibuat. Silakan login."
        )

        return redirect("main:login")

    context = {
        "name": "Muhammad Fatahillah Widodo",
        "form": form,
    }

    return render(
        request,
        "register.html",
        context
    )


def login_user(request):
    form = AuthenticationForm(
        request,
        data=request.POST or None
    )

    if request.method == "POST" and form.is_valid():
        user = form.get_user()

        login(request, user)

        response = redirect("main:show_main")

        response.set_cookie(
            "last_login",
            datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        return response

    context = {
        "name": "Muhammad Fatahillah Widodo",
        "form": form,
    }

    return render(
        request,
        "login.html",
        context
    )


def logout_user(request):
    logout(request)

    response = redirect("main:show_main")
    response.delete_cookie("last_login")

    return response


@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(
        Project,
        pk=project_id
    )

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")