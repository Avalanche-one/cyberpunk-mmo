from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Faction(models.Model):
    SIDE_CHOICES = [
        ("C", "Corporations"),
        ("G", "Gangs"),
        ("N", "Nomads"),
        ("E", "Edgerunners")
    ]
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    side = models.CharField(max_length=1, choices=SIDE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.side})"


class Specialization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

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
    PATH_CHOICES = [
        ("veteran", "War Veteran"),
        ("merc", "Mercenary"),
        ("netrunner", "Netrunner"),
        ("smug", "Smuggler"),
        ("rich", "Rich Kid"),
    ]
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=9, choices=PATH_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="characters")
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name="characters",
                                       default="Solo")
    faction = models.ForeignKey(Faction, on_delete=models.CASCADE, related_name="characters")
    level = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_character_name_per_owner",
            ),
            models.CheckConstraint(
                condition=models.Q(level__gte=1, level__lte=60),
                name="character_level_between_1_and_60"
            )
        ]

    def __str__(self):
        return (f"{self.name}, "
                f"level - {self.level},  "
                f"specialization - {self.specialization}, "
                f"faction - {self.faction}")
