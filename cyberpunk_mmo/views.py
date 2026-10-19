from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from cyberpunk_mmo.forms import CharacterForm
from cyberpunk_mmo.models import Faction, Specialization, Post, Character


class IndexView(generic.TemplateView):
    template_name = "cyberpunk_mmo/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_players"] = get_user_model().objects.count()
        return context


class SetThemeView(generic.View):
    http_method_names = ["post"]
    allowed_themes = {"original", "phantom"}

    def post(self, request, *args, **kwargs):
        selected_theme = request.POST.get("theme")
        if selected_theme in self.allowed_themes:
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
