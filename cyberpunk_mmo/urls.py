from django.urls import path

from cyberpunk_mmo.views import index, FactionListView

urlpatterns = [
    path("", index, name="index"),
    path("factions/", FactionListView.as_view(), name="faction-list"),
]

app_name = "cyberpunk_mmo"
