from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.http import require_POST
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from cyberpunk_mmo.forms import RegisterForm, CharacterForm, ProfileUpdateForm
from cyberpunk_mmo.models import Faction, Specialization, Post, Character


def index(request: HttpRequest) -> HttpResponse:
    num_players = get_user_model().objects.count()
    context = {"num_players": num_players}
    return render(request, "cyberpunk_mmo/index.html", context=context)


@require_POST
def set_theme(request: HttpRequest) -> HttpResponse:
    allowed_themes = {"original", "phantom"}
    selected_theme = request.POST.get("theme")
    if selected_theme in allowed_themes:
        request.session["theme"] = selected_theme
    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)
    return redirect("cyberpunk_mmo:index")


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
        queryset = super().get_queryset().filter(owner=self.request.user)
        name = self.request.GET.get("search", "").strip()
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class CharacterDetailView(LoginRequiredMixin, generic.DetailView):
    model = Character

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(owner=self.request.user)
            .select_related("specialization", "faction")
        ).prefetch_related("specialization__skills")


class CharacterCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Character
    form_class = CharacterForm
    template_name = "cyberpunk_mmo/character_form.html"
    success_url = reverse_lazy("cyberpunk_mmo:character-list")
    success_message = "Character was created successfully."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CharacterUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = "cyberpunk_mmo/character_form.html"
    success_url = reverse_lazy("cyberpunk_mmo:character-list")
    success_message = "Character was updated successfully."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_queryset(self):
        return Character.objects.filter(owner=self.request.user)


class CharacterDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Character
    success_url = reverse_lazy("cyberpunk_mmo:character-list")
    template_name = "cyberpunk_mmo/character_confirm_delete.html"
    success_message = "Character was deleted successfully."

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


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = "cyberpunk_mmo/profile_detail.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    form_class = ProfileUpdateForm
    template_name = "cyberpunk_mmo/profile_form.html"
    success_url = reverse_lazy("cyberpunk_mmo:profile")
    success_message = "Profile was updated successfully."

    def get_object(self, queryset=None):
        return self.request.user


class ProfileDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    template_name = "cyberpunk_mmo/profile_confirm_delete.html"
    success_url = reverse_lazy("cyberpunk_mmo:index")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        messages.success(self.request, "Your account was deleted successfully.")
        return response
