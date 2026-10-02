from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http.request import HttpRequest

from cyberpunk_mmo.models import (
    User,
    Faction,
    Specialization,
    Skill,
    Character
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ("username",)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Additional info",
            {"fields": ("first_name", "last_name",)},
        ),
    )


@admin.register(Faction)
class FactionAdmin(admin.ModelAdmin):
    list_filter = ("side",)
    list_display = ("name", "side")
    search_fields = ("name",)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "display_skills")

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).prefetch_related("skills")

    @admin.display(description="Skills")
    def display_skills(self, obj) -> str:
        return ", ".join(skill.name for skill in obj.skills.all())


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "display_specializations")

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).prefetch_related("specializations")

    @admin.display(description="Specializations")
    def display_specializations(self, obj) -> str:
        return ", ".join(specialization.name for specialization in obj.specializations.all())


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "faction", "path", "level")
    fields = ("name", "faction", "path", "specialization")
    list_filter = ("specialization", "faction", "path", "level")
    search_fields = ("name",)
    list_select_related = ("specialization", "faction")
