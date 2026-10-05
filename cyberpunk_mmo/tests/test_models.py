from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db import IntegrityError, transaction
from django.utils import timezone

from cyberpunk_mmo.models import Faction, Specialization, Skill, Character, Post


class FactionModelTests(TestCase):
    def setUp(self):
        self.faction = Faction.objects.create(
            name="Kan Tao Test",
            description="Description",
            side="C",
        )

    def test_str(self):
        self.assertEqual(str(self.faction), "Kan Tao Test (Corporations)")

    def test_image_path(self):
        self.assertEqual(
            self.faction.image_path,
            "images/factions/kan-tao-test.png",
        )

    def test_side_display(self):
        self.assertEqual(self.faction.get_side_display(), "Corporations")


class SpecializationModelTests(TestCase):
    def setUp(self):
        self.specialization = Specialization.objects.create(
            name="Cool Guy", description="Test Spec"
        )

    def test_str(self):
        self.assertEqual(str(self.specialization), "Cool Guy")

    def test_image_path(self):
        self.assertEqual(
            self.specialization.image_path,
            "images/specializations/cool-guy.png",
        )


class SkillModelTest(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(
            name="Test Skill",
            description="Common Test Skill",
        )

    def test_str(self):
        self.assertEqual(str(self.skill), "Test Skill")


class CharacterModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.faction = Faction.objects.create(
            name="Test",
            description="Description",
            side="C",
        )
        self.specialization = Specialization.objects.create(
            name="Test",
        )
        self.character = Character.objects.create(
            name="Test Dummy",
            path="merc",
            sex="male",
            specialization=self.specialization,
            faction=self.faction,
            owner=self.user,
        )

    def test_str(self):
        self.assertEqual(
            str(self.character),
            "Test Dummy, level - 1, specialization - Test, faction - Test (Corporations)",
        )

    def test_owner_cannot_have_characters_with_same_name(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Character.objects.create(
                    name=self.character.name,
                    sex="male",
                    path="merc",
                    owner=self.user,
                    specialization=self.specialization,
                    faction=self.faction,
                )

    def test_different_owners_can_have_characters_with_same_name(self):
        second_user = get_user_model().objects.create_user(
            username="second_user",
            password="testpass123",
        )
        second_character = Character.objects.create(
            name=self.character.name,
            path="merc",
            owner=second_user,
            specialization=self.specialization,
            faction=self.faction,
        )
        self.assertEqual(second_character.name, self.character.name)
        self.assertNotEqual(second_character.owner, self.character.owner)
        self.assertEqual(
            Character.objects.filter(name=self.character.name).count(),
            2,
        )


class PostModelTests(TestCase):
    def setUp(self):
        self.older_post = Post.objects.create(
            name="Older Test Post", text="Older Test Post Text"
        )
        self.newer_post = Post.objects.create(
            name="Newer Test Post", text="Newer Test Post Text"
        )

    def test_str(self):
        self.assertEqual(str(self.older_post), "Older Test Post")

    def test_posts_ordered_by_created_at_descending(self):
        now = timezone.now()
        Post.objects.filter(pk=self.older_post.pk).update(
            created_at=now - timedelta(days=1),
        )
        Post.objects.filter(pk=self.newer_post.pk).update(
            created_at=now,
        )
        self.assertEqual(
            list(Post.objects.all()),
            [self.newer_post, self.older_post],
        )
