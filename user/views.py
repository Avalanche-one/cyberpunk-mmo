from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from user.forms import RegisterForm, ProfileUpdateForm


class UserCreateView(generic.CreateView):
    form_class = RegisterForm
    template_name = "user/register.html"
    success_url = reverse_lazy("user:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("cyberpunk_mmo:index")
        return super().dispatch(request, *args, **kwargs)


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = "user/profile_detail.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    form_class = ProfileUpdateForm
    template_name = "user/profile_form.html"
    success_url = reverse_lazy("user:profile")
    success_message = "Profile was updated successfully."

    def get_object(self, queryset=None):
        return self.request.user


class ProfileDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    template_name = "user/profile_confirm_delete.html"
    success_url = reverse_lazy("cyberpunk_mmo:index")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        messages.success(self.request, "Your account was deleted successfully.")
        return response
