import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project


def is_editor(user):
    return (
        user.is_authenticated
        and user.groups.filter(name="Editor").exists()
    )


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
    experiences = Experience.objects.all()

    context = {
        "name": "Muhammad Fatahillah Widodo",
        "experience_list": experiences,
        "is_editor": is_editor(request.user),
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
        "is_editor": is_editor(request.user),
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
        "page_title": "Tambah Project",
    }

    return render(request, "projects_form.html", context)

@login_required(login_url="/login/")
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "status": "error",
                "message": "Anda tidak memiliki izin."
            },
            status=403
        )

    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save()

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Project berhasil ditambahkan!",
                    "project_id": project.pk,
                },
                status=201
            )

        return JsonResponse(
            {
                "status": "error",
                "message": "Data project tidak valid.",
                "errors": form.errors,
            },
            status=400
        )

    return JsonResponse(
        {
            "status": "error",
            "message": "Method tidak diizinkan."
        },
        status=405
    )


@login_required(login_url="/login/")
def update_project(request, project_id):
    if not request.user.is_superuser and not is_editor(request.user):
        raise PermissionDenied

    project = get_object_or_404(
        Project,
        pk=project_id
    )

    form = ProjectForm(
        request.POST or None,
        instance=project
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Project berhasil diperbarui!"
        )

        return redirect("main:show_projects")

    context = {
        "name": "Muhammad Fatahillah Widodo",
        "form": form,
        "page_title": "Edit Project",
    }

    return render(request, "projects_form.html", context)


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


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()

    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(
            title__icontains=title_query
        )

    data = []

    for project in projects:
        is_starred = False

        if request.user.is_authenticated:
            is_starred = project.starred_by.filter(
                pk=request.user.pk
            ).exists()

        data.append({
            "id": project.pk,
            "title": project.title,
            "description": project.description,
            "technology": project.technology,
            "project_url": project.project_url,
            "star_count": project.starred_by.count(),
            "is_starred": is_starred,
        })

    return JsonResponse(
        {
            "projects": data,
            "is_authenticated": request.user.is_authenticated,
            "is_superuser": request.user.is_superuser,
            "is_editor": is_editor(request.user),
        }
    )

    return HttpResponse(
        projects_json,
        content_type="application/json"
    )


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not request.user.is_superuser and not is_editor(request.user):
        raise PermissionDenied

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


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

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
            is_starred = False
            message = "Star berhasil dibatalkan."
        else:
            project.starred_by.add(request.user)
            is_starred = True
            message = "Project berhasil diberi Star."

        return JsonResponse(
            {
                "status": "success",
                "message": message,
                "is_starred": is_starred,
                "star_count": project.starred_by.count(),
            }
        )

    return JsonResponse(
        {
            "status": "error",
            "message": "Method tidak diizinkan."
        },
        status=405
    )