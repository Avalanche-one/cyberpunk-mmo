from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from cyberpunk_mmo.forms import RegisterForm, CharacterForm
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
        return (super()
                .get_queryset()
                .filter(owner=self.request.user))



class CharacterDetailView(LoginRequiredMixin, generic.DetailView):
    model = Character

    def get_queryset(self):
        return (super()
                .get_queryset()
                .filter(owner=self.request.user)
                .select_related("specialization", "faction"))


class CharacterCreateView(LoginRequiredMixin, generic.CreateView):
    model = Character
    form_class = CharacterForm
    template_name = "cyberpunk_mmo/character_form.html"
    success_url = reverse_lazy("cyberpunk_mmo:character-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CharacterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = "cyberpunk_mmo/character_form.html"
    success_url = reverse_lazy("cyberpunk_mmo:character-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_queryset(self):
        return Character.objects.filter(owner=self.request.user)


class CharacterDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Character
    success_url = reverse_lazy("cyberpunk_mmo:character-list")
    template_name = "cyberpunk_mmo/character_confirm_delete.html"

    def get_queryset(self):
        return Character.objects.filter(owner=self.request.user)


class UserCreateView(generic.CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("cyberpunk_mmo:index")
        return super().dispatch(request, *args, **kwargs)
