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


class Specialization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    specializations = models.ManyToManyField(Specialization, related_name="skills")


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
    faction = models.ForeignKey(Faction, on_delete=models.CASCADE, related_name="characters")
