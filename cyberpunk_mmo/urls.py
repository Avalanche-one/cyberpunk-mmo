from django.urls import path

from cyberpunk_mmo.views import index, FactionListView, SpecializationListView, PostListView

urlpatterns = [
    path("", index, name="index"),
    path("factions/", FactionListView.as_view(), name="faction-list"),
    path("specializations/", SpecializationListView.as_view(), name="specialization-list"),
    path("news/", PostListView.as_view(), name="post-list"),
]

app_name = "cyberpunk_mmo"
