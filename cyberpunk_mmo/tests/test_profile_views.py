from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from cyberpunk_mmo.models import Faction, Specialization, Character


class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Old name",
            last_name="Old surname",
            email="old@example.com",
        )
        self.another_user = get_user_model().objects.create_user(
            username="another_user",
            password="testpass123",
            first_name="Another name",
            email="another@example.com",
        )
        self.faction = Faction.objects.create(
            name="Test faction",
            description="Test description",
            side="C",
        )
        self.specialization = Specialization.objects.create(
            name="Test specialization",
            description="Test description",
        )
        self.character = Character.objects.create(
            name="My Character",
            path="merc",
            owner=self.user,
            specialization=self.specialization,
            faction=self.faction,
        )

    def test_profile_requires_login(self):
        url = reverse("cyberpunk_mmo:profile")
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={url}",
        )

    def test_user_can_update_only_own_profile(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("cyberpunk_mmo:profile-update"),
            {
                "first_name": "New name",
                "last_name": "New surname",
                "email": "new@example.com",
            },
        )
        self.assertRedirects(
            response,
            reverse("cyberpunk_mmo:profile"),
        )
        self.user.refresh_from_db()
        self.another_user.refresh_from_db()
        self.assertEqual(self.user.first_name, "New name")
        self.assertEqual(self.user.last_name, "New surname")
        self.assertEqual(self.user.email, "new@example.com")
        self.assertEqual(self.another_user.first_name, "Another name")
        self.assertEqual(self.another_user.email, "another@example.com")

    def test_user_deletion_deletes_all_his_chars(self):
        user_id = self.user.pk
        self.client.force_login(self.user)
        self.client.post(reverse("cyberpunk_mmo:profile-delete"))
        self.assertFalse(Character.objects.filter(owner_id=user_id).exists())

    def test_deleted_user_is_not_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cyberpunk_mmo:profile-delete"))
        self.assertRedirects(
            response,
            reverse("cyberpunk_mmo:index"),
        )
        profile_url = reverse("cyberpunk_mmo:profile")
        response = self.client.get(profile_url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={profile_url}",
        )
