from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from cyberpunk_mmo.models import Character


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name")


class CharacterForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = self.cleaned_data["name"]
        if self.user is None:
            return name
        characters = Character.objects.filter(
            owner=self.user,
            name__iexact=name,
        )
        if self.instance.pk:
            characters = characters.exclude(pk=self.instance.pk)
        if characters.exists():
            raise ValidationError("You already have a character with this name.")
        return name

    class Meta:
        model = Character
        fields = ("name", "path", "sex", "specialization", "faction")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email")
