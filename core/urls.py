from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("cyberpunk_mmo/", include("cyberpunk_mmo.urls")),
]
