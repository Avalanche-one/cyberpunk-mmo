from django.urls import path

from cyberpunk_mmo.views import (index,
                                 FactionListView,
                                 SpecializationListView,
                                 PostListView,
                                 UserCreateView,
                                 CharacterListView,
                                 CharacterDetailView,
                                 CharacterCreateView,
                                 CharacterUpdateView,
                                 CharacterDeleteView,
                                 ProfileDetailView,
                                 ProfileUpdateView,
                                 ProfileDeleteView, set_theme)

urlpatterns = [
    path("", index, name="index"),
    path("factions/", FactionListView.as_view(), name="faction-list"),
    path("theme/", set_theme, name="set-theme"),
    path("specializations/", SpecializationListView.as_view(), name="specialization-list"),
    path("characters/", CharacterListView.as_view(), name="character-list"),
    path("characters/create/", CharacterCreateView.as_view(), name="character-create"),
    path("characters/<int:pk>/", CharacterDetailView.as_view(), name="character-detail"),
    path("characters/<int:pk>/update/", CharacterUpdateView.as_view(), name="character-update"),
    path("characters/<int:pk>/delete/", CharacterDeleteView.as_view(), name="character-delete"),
    path("news/", PostListView.as_view(), name="post-list"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("profile/", ProfileDetailView.as_view(), name="profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("profile/delete/", ProfileDeleteView.as_view(), name="profile-delete"),
]

app_name = "cyberpunk_mmo"
