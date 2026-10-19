from django.urls import path

from cyberpunk_mmo.views import (
    IndexView,
    SetThemeView,
    FactionListView,
    SpecializationListView,
    PostListView,
    CharacterListView,
    CharacterDetailView,
    CharacterCreateView,
    CharacterUpdateView,
    CharacterDeleteView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("factions/", FactionListView.as_view(), name="faction-list"),
    path("theme/", SetThemeView.as_view(), name="set-theme"),
    path(
        "specializations/", SpecializationListView.as_view(), name="specialization-list"
    ),
    path("characters/", CharacterListView.as_view(), name="character-list"),
    path("characters/create/", CharacterCreateView.as_view(), name="character-create"),
    path(
        "characters/<int:pk>/", CharacterDetailView.as_view(), name="character-detail"
    ),
    path(
        "characters/<int:pk>/update/",
        CharacterUpdateView.as_view(),
        name="character-update",
    ),
    path(
        "characters/<int:pk>/delete/",
        CharacterDeleteView.as_view(),
        name="character-delete",
    ),
    path("news/", PostListView.as_view(), name="post-list"),
]

app_name = "cyberpunk_mmo"
