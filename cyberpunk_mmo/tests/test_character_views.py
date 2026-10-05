from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cyberpunk_mmo.models import (Character,
                                  Faction,
                                  Specialization)


class CharacterListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.another_user = get_user_model().objects.create_user(
            username="another_user",
            password="testpass123",
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
        self.another_character = Character.objects.create(
            name="Another Character",
            path="merc",
            owner=self.another_user,
            specialization=self.specialization,
            faction=self.faction,
        )

    def test_login_required(self):
        url = reverse("cyberpunk_mmo:character-list")
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={url}",
        )

    def test_user_can_see_only_his_characters(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("cyberpunk_mmo:character-list")
        )
        characters = response.context["character_list"]
        self.assertIn(self.character, characters)
        self.assertNotIn(self.another_character, characters)
