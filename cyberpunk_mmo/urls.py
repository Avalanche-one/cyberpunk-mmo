from django.urls import path

from cyberpunk_mmo.views import (index,
                                 FactionListView,
                                 SpecializationListView,
                                 PostListView,
                                 UserCreateView,
                                 CharacterListView,
                                 CharacterDetailView,
                                 CharacterCreateView)

urlpatterns = [
    path("", index, name="index"),
    path("factions/", FactionListView.as_view(), name="faction-list"),
    path("specializations/", SpecializationListView.as_view(), name="specialization-list"),
    path("characters/", CharacterListView.as_view(), name="character-list"),
    path("characters/create/", CharacterCreateView.as_view(), name="character-create"),
    path("characters/<int:pk>/", CharacterDetailView.as_view(), name="character-detail"),
    path("news/", PostListView.as_view(), name="post-list"),
    path("register/", UserCreateView.as_view(), name="register"),
]

app_name = "cyberpunk_mmo"
