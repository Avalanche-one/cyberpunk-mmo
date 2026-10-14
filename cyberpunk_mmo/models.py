from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    name = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


class Faction(models.Model):
    SIDE_CHOICES = [
        ("C", "Corporations"),
        ("G", "Gangs"),
        ("N", "Nomads"),
        ("E", "Edgerunners"),
    ]
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    side = models.CharField(max_length=1, choices=SIDE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    @property
    def image_path(self) -> str:
        return f"images/factions/" f"{slugify(self.name)}.png"

    def __str__(self) -> str:
        return f"{self.name} ({self.get_side_display()})"


class Specialization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    @property
    def image_path(self) -> str:
        return f"images/specializations/" f"{slugify(self.name)}.png"

    def __str__(self) -> str:
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    specialization = models.ManyToManyField(Specialization, related_name="skills")

    def __str__(self) -> str:
        return self.name


class Character(models.Model):
    AVATAR_NAMES = {
        "C": "corporations",
        "G": "gangs",
        "N": "nomads",
        "E": "edgerunners",
    }
    PATH_CHOICES = [
        ("veteran", "War Veteran"),
        ("merc", "Mercenary"),
        ("netrunner", "Netrunner"),
        ("smug", "Smuggler"),
        ("rich", "Rich Kid"),
    ]
    SEX_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    name = models.CharField(max_length=25)
    sex = models.CharField(max_length=7, choices=SEX_CHOICES, default="male")
    created_at = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=9, choices=PATH_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="characters")
    specialization = models.ForeignKey(
        Specialization, on_delete=models.CASCADE, related_name="characters"
    )
    faction = models.ForeignKey(
        Faction, on_delete=models.CASCADE, related_name="characters"
    )
    level = models.IntegerField(default=1)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_character_name_per_owner",
            ),
            models.CheckConstraint(
                condition=models.Q(level__gte=1, level__lte=60),
                name="character_level_between_1_and_60",
            ),
        ]

    @property
    def avatar_path(self):
        specialization_name = slugify(self.specialization.name)
        side_name = self.AVATAR_NAMES[self.faction.side]
        return (
            "images/characters/avatars/"
            f"{specialization_name}-"
            f"{self.sex}-"
            f"{side_name}.jpg"
        )

    def __str__(self):
        return (
            f"{self.name}, "
            f"level - {self.level}, "
            f"specialization - {self.specialization}, "
            f"faction - {self.faction}"
        )
