from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from cyberpunk_mmo.models import Specialization


class SpecializationCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.url = reverse("cyberpunk_mmo:specialization-create")
        self.valid_data = {
            "name": "Cyber Samurai",
            "description": "A specialist in cyber-enhanced close combat.",
        }

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            f"{reverse('user:login')}?next={self.url}",
        )

    def test_user_without_permission_receives_403(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_user_with_permission_can_create_specialization(self):
        permission = Permission.objects.get(
            content_type__app_label="cyberpunk_mmo",
            codename="add_specialization",
        )
        self.user.user_permissions.add(permission)
        self.client.force_login(self.user)

        response = self.client.post(self.url, self.valid_data)

        self.assertRedirects(
            response,
            reverse("cyberpunk_mmo:specialization-list"),
        )
        self.assertTrue(
            Specialization.objects.filter(name=self.valid_data["name"]).exists()
        )
