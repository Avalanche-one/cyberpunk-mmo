from django.contrib.auth import get_user_model
from django.test import TestCase

from cyberpunk_mmo.forms import CharacterForm
from cyberpunk_mmo.models import Faction, Specialization, Character


class CharacterFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
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
            name="Test Dummy",
            path="merc",
            sex="male",
            specialization=self.specialization,
            faction=self.faction,
            owner=self.user,
        )

    def test_form_accepts_valid_data(self):
        form = CharacterForm(
            data={
                "name": "Test Character",
                "path": "merc",
                "sex": "female",
                "specialization": self.specialization.pk,
                "faction": self.faction.pk,
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_characters_with_same_name_not_allowed(self):
        form = CharacterForm(
            data={
                "name": "test dummy",
                "path": "merc",
                "sex": "female",
                "specialization": self.specialization.pk,
                "faction": self.faction.pk,
            },
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_same_name_allowed_while_updating_existing_character(self):
        form = CharacterForm(
            data={
                "name": self.character.name,
                "path": "merc",
                "sex": "male",
                "specialization": self.specialization.pk,
                "faction": self.faction.pk,
            },
            instance=self.character,
            user=self.user,
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_same_name_allowed_for_another_user(self):
        another_user = get_user_model().objects.create_user(
            username="testuser2",
            password="testpass123",
        )
        form = CharacterForm(
            data={
                "name": "Test Dummy",
                "path": "merc",
                "sex": "female",
                "specialization": self.specialization.pk,
                "faction": self.faction.pk,
            },
            user=another_user,
        )
        self.assertTrue(form.is_valid(), form.errors)
