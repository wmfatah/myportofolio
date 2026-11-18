from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import Project, Experience

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

        self.project = Project.objects.create(
            title="Simulasi Penyebaran Virus",
            description="Membuat simulasi penyebaran virus menggunakan Java dan Greenfoot.",
            technology="Java, Greenfoot",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(
            response,
            f'href="{reverse("main:show_experience")}"'
        )

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"'
        )

        api_response = self.client.get("/api/experiences/")

        self.assertEqual(api_response.status_code, 200)

        experiences = api_response.json()["experiences"]

        experience = next(
            (
                item for item in experiences
                if item["title"] == self.experience.title
            ),
            None
        )

        self.assertIsNotNone(experience)
        self.assertEqual(
            experience["description"],
            self.experience.description
        )
        self.assertIn("category_display", experience)
        self.assertTrue(experience["is_ongoing"])

    def test_empty_experience_page(self):
        Experience.objects.all().delete()

        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)

        api_response = self.client.get("/api/experiences/")

        self.assertEqual(api_response.status_code, 200)
        self.assertEqual(
            api_response.json()["experiences"],
            []
        )

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)

        response = self.client.get("/api/experiences/")

        self.assertEqual(response.status_code, 200)

        experiences = response.json()["experiences"]

        experience = next(
            (
                item for item in experiences
                if item["title"] == self.experience.title
            ),
            None
        )

        self.assertIsNotNone(experience)
        self.assertFalse(experience["is_ongoing"])

    def test_projects_page_is_accessible(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_project_data_appears_on_page(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)

        api_response = self.client.get(
            reverse("api:project-list")
        )

        self.assertEqual(api_response.status_code, 200)

        projects = api_response.json()

        project = next(
            (
                item for item in projects
                if item["id"] == self.project.id
            ),
            None
        )

        self.assertIsNotNone(project)
        self.assertEqual(project["title"], self.project.title)
        self.assertEqual(
            project["description"],
            self.project.description
        )
        self.assertEqual(
            project["technology"],
            self.project.technology
        )

    def test_empty_projects_page(self):
        Project.objects.all().delete()

        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)

        api_response = self.client.get(
            reverse("api:project-list")
        )

        self.assertEqual(api_response.status_code, 200)
        self.assertEqual(api_response.json(), [])
