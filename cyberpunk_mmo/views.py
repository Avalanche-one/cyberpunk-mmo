from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from cyberpunk_mmo.forms import RegisterForm
from cyberpunk_mmo.models import (Faction,
                                  Specialization,
                                  Post,
                                  Character)


def index(request: HttpRequest) -> HttpResponse:
    num_players = get_user_model().objects.count()
    context = {
        "num_players": num_players
    }
    return render(request, "cyberpunk_mmo/index.html", context=context)


class FactionListView(generic.ListView):
    model = Faction
    paginate_by = 10


class SpecializationListView(generic.ListView):
    model = Specialization


class PostListView(generic.ListView):
    model = Post
    paginate_by = 5


class CharacterListView(LoginRequiredMixin, generic.ListView):
    model = Character
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class UserCreateView(generic.CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
